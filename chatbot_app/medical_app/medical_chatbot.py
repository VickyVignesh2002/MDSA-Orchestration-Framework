"""
Medical Chatbot Application

Comprehensive medical coding, billing, and claims processing chatbot
using the MDSA framework.

Features:
- Medical coding (ICD-10, CPT, HCPCS)
- Medical billing calculations
- Insurance claims processing
- Autonomous multi-step workflows
- RAG-enhanced responses

Author: MDSA Framework Team
Date: 2025-12-06
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

import gradio as gr
import logging
from typing import List, Tuple
from datetime import datetime

from mdsa.core.orchestrator import TinyBERTOrchestrator as Orchestrator
from mdsa.memory.dual_rag import DualRAG
from chatbot_app.medical_app.domains.medical_domains import get_all_medical_domains
from chatbot_app.medical_app.knowledge_base.medical_codes import (
    populate_rag_system,
    search_codes,
    get_code_by_id
)
from chatbot_app.medical_app.workflows.autonomous_engine import (
    AutonomousWorkflowEngine,
    create_patient_encounter_workflow,
    create_billing_inquiry_workflow,
    create_claim_denial_workflow
)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class MedicalChatbot:
    """Medical Chatbot with MDSA Framework."""

    def __init__(self):
        """Initialize medical chatbot."""
        logger.info("Initializing Medical Chatbot...")

        # Initialize MDSA components
        self.orchestrator = Orchestrator(
            enable_reasoning=True,
            complexity_threshold=0.3
        )

        # Initialize RAG system
        self.dual_rag = DualRAG()

        # Register medical domains
        logger.info("Registering medical domains...")
        medical_domains = get_all_medical_domains()

        for domain_config in medical_domains:
            # Register with orchestrator (if method exists)
            # self.orchestrator.register_domain(domain_config)

            # Register with RAG
            self.dual_rag.register_domain(domain_config.domain_id)

            # Populate knowledge base
            logger.info(f"Populating knowledge base for {domain_config.domain_id}")
            populate_rag_system(self.dual_rag, domain_config.domain_id)

        # Initialize workflow engine
        self.workflow_engine = AutonomousWorkflowEngine(self.orchestrator)

        # Chat history
        self.chat_history: List[Tuple[str, str]] = []

        logger.info("Medical Chatbot initialized successfully!")

    def process_message(
        self,
        message: str,
        history: List[Tuple[str, str]]
    ) -> Tuple[str, List[Tuple[str, str]]]:
        """
        Process user message.

        Args:
            message: User input
            history: Chat history

        Returns:
            Tuple of (response, updated_history)
        """
        try:
            # Log query
            logger.info(f"Processing query: {message[:100]}...")

            # Process with orchestrator
            result = self.orchestrator.process_request(message)

            # Format response
            if result['status'] == 'success':
                response = self._format_response(result)
            else:
                response = f"Error: {result.get('error', 'Unknown error occurred')}"

            # Update history
            history.append((message, response))

            return response, history

        except Exception as e:
            logger.error(f"Error processing message: {e}")
            error_response = f"Sorry, an error occurred: {str(e)}"
            history.append((message, error_response))
            return error_response, history

    def _format_response(self, result: Dict) -> str:
        """Format orchestrator response for display."""
        response = result['response']

        # Add metadata
        footer = f"\n\n---\n"
        footer += f"Domain: {result['domain'].title()}"
        footer += f" | Latency: {result['latency_ms']:.0f}ms"

        if result.get('reasoning_used'):
            footer += f" | Reasoning: Yes (complexity: {result['complexity_score']:.2f})"

        return response + footer

    def code_lookup(self, code_id: str) -> str:
        """
        Quick code lookup.

        Args:
            code_id: Code ID (e.g., 'E11.9', '99213')

        Returns:
            Code details
        """
        code = get_code_by_id(code_id)

        if code:
            result = f"{code.code_type} Code: {code.code}\n"
            result += f"Description: {code.description}\n"
            result += f"Category: {code.category}\n"

            if code.typical_charge > 0:
                result += f"Typical Charge: ${code.typical_charge:.2f}\n"

            if code.requires_auth:
                result += "**Prior Authorization Required**\n"

            if code.notes:
                result += f"Notes: {code.notes}\n"

            return result
        else:
            return f"Code '{code_id}' not found in knowledge base."

    def search_knowledge(self, query: str, code_type: str = None) -> str:
        """
        Search medical codes.

        Args:
            query: Search term
            code_type: Filter by type

        Returns:
            Search results
        """
        results = search_codes(query, code_type=code_type)

        if not results:
            return f"No codes found matching '{query}'"

        output = f"Found {len(results)} results for '{query}':\n\n"

        for code in results[:10]:  # Limit to 10 results
            output += f"{code.code_type} {code.code}: {code.description}\n"

        if len(results) > 10:
            output += f"\n... and {len(results) - 10} more results"

        return output

    async def run_workflow(self, workflow_name: str) -> str:
        """
        Execute a predefined workflow.

        Args:
            workflow_name: Workflow identifier

        Returns:
            Workflow results
        """
        # Create workflow based on name
        if workflow_name == "patient_encounter":
            steps = create_patient_encounter_workflow()
            description = "Complete Patient Encounter"
        elif workflow_name == "billing_inquiry":
            steps = create_billing_inquiry_workflow()
            description = "Billing Inquiry"
        elif workflow_name == "claim_denial":
            steps = create_claim_denial_workflow()
            description = "Claim Denial Resolution"
        else:
            return f"Unknown workflow: {workflow_name}"

        # Create and execute workflow
        workflow_id = f"{workflow_name}_{datetime.now().timestamp()}"

        self.workflow_engine.create_workflow(
            workflow_id=workflow_id,
            name=description,
            description=f"Autonomous {description} workflow",
            steps=steps
        )

        # Execute
        logger.info(f"Executing workflow: {description}")
        result = await self.workflow_engine.execute_workflow(workflow_id)

        # Format results
        output = f"Workflow: {description}\n"
        output += f"Status: {result.get('workflow_name', 'Unknown')}\n\n"

        for step_result in result.get('results', []):
            output += f"{step_result['step_id']}. {step_result['action']}:\n"
            output += f"   {step_result['response']}\n\n"

        return output

    def get_stats(self) -> str:
        """Get chatbot statistics."""
        stats = {
            'Total Messages': len(self.chat_history),
            'RAG Domains': len(self.dual_rag.local_rags),
            'Total Knowledge Items': sum(
                rag.get_stats()['document_count']
                for rag in self.dual_rag.local_rags.values()
            )
        }

        output = "Medical Chatbot Statistics:\n\n"
        for key, value in stats.items():
            output += f"{key}: {value}\n"

        return output


# ============================================================================
# Gradio Interface
# ============================================================================

def create_gradio_interface(chatbot: MedicalChatbot):
    """Create Gradio interface for medical chatbot."""

    with gr.Blocks() as demo:
        gr.Markdown("""
        # Medical Coding, Billing & Claims Chatbot
        ### Powered by MDSA Framework

        Ask questions about:
        - **Medical Coding**: ICD-10, CPT, HCPCS codes
        - **Medical Billing**: Charges, insurance, payments
        - **Claims Processing**: Submission, status, denials

        Examples:
        - "What is ICD-10 code E11.9?"
        - "Calculate billing for office visit CPT 99213"
        - "How to handle a denied claim for prior authorization?"
        """)

        with gr.Tab("Chat"):
            chatbot_ui = gr.Chatbot(
                label="Medical Assistant",
                height=500
            )

            with gr.Row():
                msg = gr.Textbox(
                    label="Your Question",
                    placeholder="Ask a medical coding/billing question...",
                    lines=2
                )
                send_btn = gr.Button("Send", variant="primary")

            clear_btn = gr.Button("Clear Chat")

            # Chat functionality
            def respond(message, history):
                response, updated_history = chatbot.process_message(message, history)
                return "", updated_history

            msg.submit(respond, [msg, chatbot_ui], [msg, chatbot_ui])
            send_btn.click(respond, [msg, chatbot_ui], [msg, chatbot_ui])
            clear_btn.click(lambda: [], None, chatbot_ui)

        with gr.Tab("Code Lookup"):
            gr.Markdown("### Quick Code Lookup")

            code_input = gr.Textbox(
                label="Code ID",
                placeholder="Enter code (e.g., E11.9, 99213, A4253)"
            )
            lookup_btn = gr.Button("Lookup", variant="primary")
            lookup_output = gr.Textbox(
                label="Code Details",
                lines=10
            )

            lookup_btn.click(
                chatbot.code_lookup,
                inputs=code_input,
                outputs=lookup_output
            )

        with gr.Tab("Search"):
            gr.Markdown("### Search Medical Codes")

            with gr.Row():
                search_input = gr.Textbox(
                    label="Search Query",
                    placeholder="Enter search term (e.g., diabetes, office visit)"
                )
                code_type_filter = gr.Dropdown(
                    label="Code Type",
                    choices=["All", "ICD-10", "CPT", "HCPCS"],
                    value="All"
                )

            search_btn = gr.Button("Search", variant="primary")
            search_output = gr.Textbox(
                label="Search Results",
                lines=15
            )

            def search_wrapper(query, code_type):
                ct = None if code_type == "All" else code_type
                return chatbot.search_knowledge(query, ct)

            search_btn.click(
                search_wrapper,
                inputs=[search_input, code_type_filter],
                outputs=search_output
            )

        with gr.Tab("Workflows"):
            gr.Markdown("""
            ### Autonomous Workflows

            Run complex multi-step workflows automatically.
            """)

            workflow_choice = gr.Radio(
                label="Select Workflow",
                choices=[
                    ("Complete Patient Encounter", "patient_encounter"),
                    ("Billing Inquiry", "billing_inquiry"),
                    ("Claim Denial Resolution", "claim_denial")
                ],
                value="patient_encounter"
            )

            run_workflow_btn = gr.Button("Run Workflow", variant="primary")
            workflow_output = gr.Textbox(
                label="Workflow Results",
                lines=20
            )

            async def run_workflow_wrapper(workflow_name):
                return await chatbot.run_workflow(workflow_name)

            run_workflow_btn.click(
                run_workflow_wrapper,
                inputs=workflow_choice,
                outputs=workflow_output
            )

        with gr.Tab("Statistics"):
            gr.Markdown("### Chatbot Statistics")

            stats_btn = gr.Button("Refresh Statistics")
            stats_output = gr.Textbox(
                label="Statistics",
                lines=10
            )

            stats_btn.click(
                chatbot.get_stats,
                outputs=stats_output
            )

    return demo


# ============================================================================
# Main Application
# ============================================================================

def main():
    """Run medical chatbot application."""
    print("=" * 70)
    print("Medical Chatbot - MDSA Framework")
    print("=" * 70)

    # Initialize chatbot
    chatbot = MedicalChatbot()

    # Create and launch Gradio interface
    demo = create_gradio_interface(chatbot)

    print("\nLaunching Gradio interface...")
    print("Access at: http://localhost:7860")
    print("=" * 70)

    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,  # Set to True to create public link
        title="Medical Chatbot - MDSA Framework"
    )


if __name__ == "__main__":
    main()

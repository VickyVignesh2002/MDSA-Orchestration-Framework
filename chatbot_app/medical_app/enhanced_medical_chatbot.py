"""
Enhanced Medical Chatbot Application

Production-ready medical assistant using specialized SLMs:
- Meerkat-8B for clinical diagnosis
- MediPhi-Instruct for medical coding/billing
- OpenBioLLM-8B for biomedical extraction
- BioMedLM for radiology support
- TinyLlama-Health for quick medical Q&A

Features:
- Dual RAG system (Global + Local knowledge)
- Hybrid orchestration (TinyBERT + Phi-2 reasoning)
- Multi-domain expertise
- Real-time statistics and monitoring
"""

import gradio as gr
from typing import List, Tuple, Dict, Any
import json
from datetime import datetime

# MDSA Framework imports
from mdsa.core.orchestrator import TinyBERTOrchestrator as Orchestrator
from mdsa.memory.dual_rag import DualRAG
from mdsa.ui.enhanced_dashboard import EnhancedDashboard

# Medical-specific imports
from domains.enhanced_medical_domains import (
    get_all_enhanced_medical_domains,
    DOMAIN_PRIORITY
)
from knowledge_base.enhanced_medical_kb import (
    initialize_medical_knowledge_base,
    get_code_by_number,
    search_codes_by_description
)


class EnhancedMedicalChatbot:
    """
    Enhanced medical chatbot with specialized SLMs and RAG.
    """

    def __init__(
        self,
        enable_reasoning: bool = True,
        prefer_gpu: bool = True,
        force_device: str = None
    ):
        """
        Initialize enhanced medical chatbot.

        Args:
            enable_reasoning: Enable hybrid orchestration with Phi-2 reasoning
            prefer_gpu: Prefer GPU if available
            force_device: Force specific device (cpu/cuda)
        """
        print("[INIT] Initializing Enhanced Medical Chatbot...")

        # Initialize orchestrator with hybrid reasoning
        self.orchestrator = Orchestrator(
            enable_reasoning=enable_reasoning,
            complexity_threshold=0.3  # Queries >0.3 complexity use Phi-2
        )

        # Initialize Dual RAG system (10k global docs, default 1k local docs)
        self.dual_rag = DualRAG(max_global_docs=10000)
        print("[INIT] Initializing medical knowledge base...")
        initialize_medical_knowledge_base(self.dual_rag)

        # Register all medical domains
        print("[INIT] Registering medical domains...")
        self.domains = get_all_enhanced_medical_domains(prefer_gpu, force_device)
        for domain in self.domains:
            print(f"  - {domain.name} ({domain.model_name})")
            self.orchestrator.domain_executor.register_domain(domain)

        # Initialize dashboard for monitoring
        self.dashboard = EnhancedDashboard(output_dir="./dashboard_output")

        # Conversation history
        self.conversation_history: List[Dict[str, Any]] = []

        print("[INIT] Enhanced Medical Chatbot ready!")
        print(f"[INIT] Registered {len(self.domains)} specialized medical domains")
        print(f"[INIT] Knowledge base: {len(self.dual_rag._global_rag._documents)} global documents")

    def process_message(
        self,
        message: str,
        history: List[Tuple[str, str]]
    ) -> Tuple[List[Tuple[str, str]], str, str]:
        """
        Process user message and return response with metadata.

        Args:
            message: User's input message
            history: Chat history

        Returns:
            Tuple of (updated_history, metadata_json, rag_context)
        """
        try:
            # Check for special commands
            if message.startswith("/code "):
                code = message.split(" ", 1)[1].strip()
                return self._handle_code_lookup(code, history)

            # Process through orchestrator
            start_time = datetime.now()
            result = self.orchestrator.process_request(message)
            latency_ms = (datetime.now() - start_time).total_seconds() * 1000

            # Get RAG context if available
            rag_context = self._get_rag_context(message, result.get('domain', 'unknown'))

            # Extract response
            response = result.get('response', 'Sorry, I could not process your request.')

            # Update dashboard
            self.dashboard.track_request(
                query=message,
                domain=result.get('domain', 'unknown'),
                model=result.get('model', 'unknown'),
                latency_ms=latency_ms,
                success=(result.get('status') == 'success'),
                correlation_id=f"req_{len(self.conversation_history)}"
            )

            # Format metadata
            metadata = {
                "domain": result.get('domain', 'unknown'),
                "model": result.get('model', 'unknown'),
                "latency_ms": round(latency_ms, 2),
                "complexity": result.get('complexity', 'N/A'),
                "used_reasoning": result.get('used_reasoning', False),
                "status": result.get('status', 'unknown')
            }

            # Save to history
            self.conversation_history.append({
                "timestamp": datetime.now().isoformat(),
                "query": message,
                "response": response,
                "metadata": metadata
            })

            # Update gradio history
            history.append((message, response))

            return history, json.dumps(metadata, indent=2), rag_context

        except Exception as e:
            error_msg = f"Error: {str(e)}"
            history.append((message, error_msg))
            return history, json.dumps({"error": str(e)}, indent=2), ""

    def _handle_code_lookup(
        self,
        code: str,
        history: List[Tuple[str, str]]
    ) -> Tuple[List[Tuple[str, str]], str, str]:
        """Handle special /code command for direct code lookup."""
        code_info = get_code_by_number(code.upper())

        if code_info:
            response = f"""
**{code_info.code_type}: {code_info.code}**

**Description:** {code_info.description}

**Category:** {code_info.category}

**Billable:** {"Yes" if code_info.billable else "No"}

**Typical Charge:** ${code_info.typical_charge:.2f}

**Medical Necessity:** {code_info.medical_necessity if code_info.medical_necessity else "N/A"}

**Authorization Required:** {"Yes" if code_info.requires_auth else "No"}
            """
        else:
            response = f"Code '{code}' not found in knowledge base. Try a general search or ask me about it!"

        history.append((f"/code {code}", response))
        metadata = {"command": "code_lookup", "code": code, "found": code_info is not None}

        return history, json.dumps(metadata, indent=2), ""

    def _get_rag_context(self, query: str, domain: str) -> str:
        """Get RAG context for the query."""
        try:
            # Search both global and local RAG
            results = self.dual_rag.retrieve(
                query=query,
                domain_id=domain,
                search_local=True,
                search_global=True,
                top_k=3
            )

            context_parts = []

            if results['global'].documents:
                context_parts.append("**Global Knowledge:**")
                for doc in results['global'].documents[:2]:
                    context_parts.append(f"- {doc.content[:200]}...")

            if results['local'].documents:
                context_parts.append("\n**Domain-Specific Knowledge:**")
                for doc in results['local'].documents[:2]:
                    context_parts.append(f"- {doc.content[:200]}...")

            return "\n".join(context_parts) if context_parts else "No RAG context retrieved"

        except:
            return "RAG context unavailable"

    def get_statistics(self) -> str:
        """Get chatbot statistics."""
        stats = self.orchestrator.get_statistics()
        return json.dumps(stats, indent=2)

    def search_codes(self, search_term: str) -> str:
        """Search medical codes by description."""
        results = search_codes_by_description(search_term)

        if not results:
            return f"No codes found matching '{search_term}'"

        output = f"**Found {len(results)} codes matching '{search_term}':**\n\n"
        for code in results[:10]:  # Limit to top 10
            output += f"- **{code.code}** ({code.code_type}): {code.description}\n"

        return output

    def export_conversation(self) -> str:
        """Export conversation history as JSON."""
        return json.dumps(self.conversation_history, indent=2)


# ============================================================================
# Gradio Interface
# ============================================================================

def create_gradio_interface(
    enable_reasoning: bool = True,
    prefer_gpu: bool = False,  # Default to CPU for compatibility
    share: bool = False
):
    """
    Create and launch Gradio interface.

    Args:
        enable_reasoning: Enable Phi-2 hybrid reasoning
        prefer_gpu: Prefer GPU if available
        share: Create public link
    """
    # Initialize chatbot
    chatbot = EnhancedMedicalChatbot(
        enable_reasoning=enable_reasoning,
        prefer_gpu=prefer_gpu
    )

    # Create Gradio interface
    with gr.Blocks() as demo:
        gr.Markdown("""
        # 🏥 Enhanced Medical Assistant

        Powered by Specialized Medical SLMs:
        - **Meerkat-8B**: Clinical diagnosis and reasoning
        - **MediPhi-Instruct**: Medical coding and billing
        - **OpenBioLLM-8B**: Biomedical text extraction
        - **BioMedLM**: Radiology support
        - **TinyLlama-Health**: Quick medical Q&A

        **Features**: Hybrid AI orchestration, Dual RAG knowledge base, Real-time statistics
        """)

        with gr.Tabs():
            # Chat Tab
            with gr.Tab("💬 Medical Chat"):
                with gr.Row():
                    with gr.Column(scale=2):
                        chatbox = gr.Chatbot(
                            label="Conversation",
                            height=500,
                            avatar_images=(None, "🏥")
                        )
                        msg = gr.Textbox(
                            label="Your Message",
                            placeholder="Ask me about diagnoses, medical codes, procedures, etc. or use /code <CODE> for direct lookup",
                            lines=2
                        )
                        with gr.Row():
                            submit = gr.Button("Send", variant="primary")
                            clear = gr.Button("Clear Chat")

                    with gr.Column(scale=1):
                        gr.Markdown("### 📊 Response Metadata")
                        metadata_box = gr.JSON(label="Metadata")

                        gr.Markdown("### 📚 RAG Context")
                        rag_box = gr.Textbox(
                            label="Knowledge Retrieved",
                            lines=8,
                            interactive=False
                        )

                # Submit handlers
                submit.click(
                    chatbot.process_message,
                    inputs=[msg, chatbox],
                    outputs=[chatbox, metadata_box, rag_box]
                )
                msg.submit(
                    chatbot.process_message,
                    inputs=[msg, chatbox],
                    outputs=[chatbox, metadata_box, rag_box]
                )
                clear.click(lambda: ([], None, ""), outputs=[chatbox, metadata_box, rag_box])

            # Code Lookup Tab
            with gr.Tab("🔍 Code Lookup"):
                gr.Markdown("### Search Medical Codes")
                search_input = gr.Textbox(
                    label="Search by description",
                    placeholder="Enter keywords (e.g., 'diabetes', 'chest pain', 'office visit')"
                )
                search_btn = gr.Button("Search", variant="primary")
                search_results = gr.Markdown(label="Results")

                search_btn.click(
                    chatbot.search_codes,
                    inputs=[search_input],
                    outputs=[search_results]
                )

                gr.Markdown("### Direct Code Lookup")
                gr.Markdown("**Quick Reference:**")
                gr.Markdown("""
                - **ICD-10**: E11.9, I10, J44.0, N18.3, E78.5
                - **CPT**: 99213, 99214, 80053, 93000, 71046
                - **HCPCS**: J3301, G0438, A4253
                """)

            # Statistics Tab
            with gr.Tab("📈 Statistics"):
                gr.Markdown("### System Performance")
                stats_box = gr.JSON(label="Orchestrator Statistics")
                refresh_stats = gr.Button("Refresh Statistics")

                refresh_stats.click(
                    chatbot.get_statistics,
                    outputs=[stats_box]
                )

            # Export Tab
            with gr.Tab("💾 Export"):
                gr.Markdown("### Export Conversation History")
                export_box = gr.Code(language="json", label="Conversation JSON")
                export_btn = gr.Button("Export", variant="primary")

                export_btn.click(
                    chatbot.export_conversation,
                    outputs=[export_box]
                )

            # Help Tab
            with gr.Tab("❓ Help"):
                gr.Markdown("""
                ## How to Use

                ### Chat Interface
                - Type your medical question naturally
                - The system will automatically route to the best specialized domain
                - Use `/code <CODE>` for direct code lookup (e.g., `/code E11.9`)

                ### Example Queries

                **Clinical Diagnosis:**
                - "What are the differential diagnoses for chest pain?"
                - "Explain the symptoms of Type 2 diabetes"

                **Medical Coding:**
                - "What ICD-10 code should I use for hypertension?"
                - "Suggest CPT codes for a comprehensive metabolic panel"
                - "Help me write a medical necessity statement for a chest X-ray"

                **Biomedical Extraction:**
                - "Extract diagnoses and procedures from this clinical note: [paste note]"
                - "Summarize this radiology report"

                **Quick Medical Q&A:**
                - "What is hemoglobin A1c?"
                - "Explain what COPD means"

                ### System Features
                - **Hybrid Orchestration**: Simple queries use fast TinyBERT (<50ms), complex queries use Phi-2 reasoning
                - **Dual RAG**: Shared medical codes + domain-specific knowledge
                - **Multi-Domain**: 5 specialized medical SLMs working together
                - **Real-Time Stats**: Monitor performance and routing decisions

                ### Supported Domains
                1. **Clinical Diagnosis** (Meerkat-8B) - Diagnosis, symptoms, clinical reasoning
                2. **Medical Coding** (MediPhi-Instruct) - ICD/CPT/HCPCS codes, billing
                3. **Biomedical Extraction** (OpenBioLLM-8B) - Text analysis, entity extraction
                4. **Radiology Support** (BioMedLM) - Radiology reports, imaging
                5. **Medical Q&A Lite** (TinyLlama) - Quick definitions, simple questions
                """)

        gr.Markdown("""
        ---
        **Disclaimer**: This is an AI assistant for educational and support purposes only.
        Always consult licensed healthcare professionals for medical advice and actual diagnosis/treatment.
        """)

    # Launch
    print("\n" + "="*60)
    print("🏥 ENHANCED MEDICAL CHATBOT - READY")
    print("="*60)
    print(f"Hybrid Reasoning: {'Enabled' if enable_reasoning else 'Disabled'}")
    print(f"GPU Acceleration: {'Enabled' if prefer_gpu else 'Disabled (CPU only)'}")
    print(f"Registered Domains: {len(chatbot.domains)}")
    print("="*60 + "\n")

    demo.launch(
        share=share,
        server_name="0.0.0.0",
        server_port=7860,
        title="Enhanced Medical Assistant",
        theme=gr.themes.Soft(
            primary_hue="blue",
            secondary_hue="green"
        )
    )


if __name__ == "__main__":
    # Launch with default settings
    create_gradio_interface(
        enable_reasoning=True,  # Enable Phi-2 hybrid orchestration
        prefer_gpu=False,  # Use CPU by default (change to True if GPU available)
        share=False  # Set to True to create public link
    )

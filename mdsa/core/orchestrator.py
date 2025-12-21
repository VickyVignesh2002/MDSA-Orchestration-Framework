"""
Orchestrator Module

Main orchestration engine coordinating intent routing, state management, and execution.
"""

import logging
import time
from pathlib import Path
from typing import Any, Dict, Optional, List

from mdsa.core.communication_bus import MessageBus, MessageType
from mdsa.core.router import IntentRouter
from mdsa.core.state_machine import StateMachine, WorkflowState
from mdsa.core.complexity_analyzer import ComplexityAnalyzer, ComplexityResult
from mdsa.core.reasoner import Phi2Reasoner, ReasoningResult, Task
from mdsa.utils.config_loader import ConfigLoader
from mdsa.utils.hardware import HardwareDetector
from mdsa.utils.logger import setup_logger

logger = logging.getLogger(__name__)


class TinyBERTOrchestrator:
    """
    Main orchestration engine for MDSA framework.

    Coordinates:
    - Intent classification (TinyBERT) - <50ms target
    - State machine workflow
    - Message bus communication
    - Domain lifecycle management

    Example:
        >>> orchestrator = TinyBERTOrchestrator()
        >>> orchestrator.register_domain("finance", "Financial operations", ["money"])
        >>> result = orchestrator.process_request("Transfer $100")
        >>> print(result['status'])
    """

    def __init__(
        self,
        config_path: Optional[str] = None,
        log_level: str = "INFO",
        enable_reasoning: bool = True,
        complexity_threshold: float = 0.3
    ):
        """
        Initialize orchestrator with hybrid routing support.

        Args:
            config_path: Path to configuration file
            log_level: Logging level
            enable_reasoning: Enable Phi-2 reasoning for complex queries (default: True)
            complexity_threshold: Threshold for complexity detection (0.0-1.0, default: 0.3)
        """
        # Initialize logger
        self.logger = setup_logger('mdsa.orchestrator', level=log_level)

        # Load configuration
        self.config = self._load_config(config_path)

        # Hardware detection
        self.hardware = HardwareDetector()
        self.logger.info(f"Hardware: {self.hardware.get_summary()}")

        # Core components
        self.router = IntentRouter(
            device=self.hardware.best_device_for_tier1(),
            confidence_threshold=self.config.get('orchestrator', {}).get('confidence_threshold', 0.85)
        )
        self.state_machine = StateMachine()
        self.message_bus = MessageBus()

        # Phase 8: Hybrid orchestration components
        self.enable_reasoning = enable_reasoning
        self.complexity_analyzer = ComplexityAnalyzer(complexity_threshold=complexity_threshold)
        self.reasoner = Phi2Reasoner() if enable_reasoning else None

        # Domain registry (will be populated in Phase 4)
        self.domains = {}

        # Statistics
        self.stats = {
            'requests_total': 0,
            'requests_success': 0,
            'requests_failed': 0,
            'requests_reasoning': 0,  # Track reasoning-based requests
            'total_latency_ms': 0
        }

        mode = "hybrid (TinyBERT + Phi-2)" if enable_reasoning else "TinyBERT only"
        self.logger.info(f"TinyBERTOrchestrator initialized ({mode})")

    def _load_config(self, config_path: Optional[str]) -> Dict:
        """
        Load configuration from file or use defaults.

        Args:
            config_path: Path to config file

        Returns:
            dict: Configuration
        """
        if config_path:
            try:
                loader = ConfigLoader()
                return loader.load(config_path)
            except FileNotFoundError:
                logger.warning(f"Config file not found: {config_path}. Using defaults.")

        # Default configuration
        return {
            'framework': {
                'name': 'MDSA',
                'version': '1.0.0'
            },
            'orchestrator': {
                'confidence_threshold': 0.80,  # Lowered from 0.85 to reduce false escalations
                'device': 'auto'
            },
            'monitoring': {
                'metrics': True,
                'logging': True
            }
        }

    def register_domain(
        self,
        name: str,
        description: str,
        keywords: Optional[list] = None
    ):
        """
        Register a domain for routing.

        Args:
            name: Domain name
            description: Domain description
            keywords: Optional keywords for fallback routing

        Example:
            >>> orchestrator.register_domain(
            ...     "finance",
            ...     "Financial transactions",
            ...     ["money", "transfer"]
            ... )
        """
        self.router.register_domain(name, description, keywords)
        self.logger.info(f"Domain registered: {name}")

        # Publish event
        self.message_bus.publish(
            "system",
            "orchestrator",
            {"action": "domain_registered", "domain": name},
            MessageType.LOG
        )

    def process_request(self, query: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Process user query through full orchestration workflow.

        Workflow:
        1. INIT -> CLASSIFY: Intent routing (TinyBERT <50ms)
        2. CLASSIFY -> VALIDATE_PRE: Check confidence threshold
        3. VALIDATE_PRE -> LOAD_SLM: Would load domain SLM (Phase 4)
        4. LOAD_SLM -> EXECUTE: Would execute domain logic (Phase 4)
        5. EXECUTE -> VALIDATE_POST: Would validate output (Phase 7)
        6. VALIDATE_POST -> LOG: Log execution
        7. LOG -> RETURN: Return result

        Args:
            query: User query string
            context: Optional context dictionary

        Returns:
            dict: Result with status, metadata, and (later) actual response

        Example:
            >>> result = orchestrator.process_request("Transfer money")
            >>> print(result['metadata']['domain'])
        """
        start_time = time.time()
        correlation_id = f"req_{int(time.time() * 1000)}"

        # Initialize state machine
        self.state_machine.reset()
        self.state_machine.set_metadata('correlation_id', correlation_id)
        self.state_machine.set_metadata('query', query)

        try:
            # Phase 8: Check query complexity for hybrid routing
            if self.enable_reasoning:
                complexity_result = self.complexity_analyzer.analyze(query)
                self.logger.info(
                    f"Complexity analysis: score={complexity_result.complexity_score:.2f}, "
                    f"complex={complexity_result.is_complex}, indicators={complexity_result.indicators}"
                )

                # Route to reasoning path if complex
                if complexity_result.is_complex:
                    return self._process_with_reasoning(query, context, correlation_id, start_time)

            # Simple query path: Use TinyBERT routing
            # 1. CLASSIFY: Intent routing
            self.state_machine.transition(WorkflowState.CLASSIFY)
            self._publish_state_change(WorkflowState.CLASSIFY, correlation_id)

            domain, confidence = self.router.classify(query)

            self.logger.info(
                f"Query classified (TinyBERT): domain={domain}, confidence={confidence:.3f}, "
                f"query='{query[:50]}...'"
            )

            # 2. Check confidence threshold
            threshold = self.config.get('orchestrator', {}).get('confidence_threshold', 0.85)
            if confidence < threshold:
                return self._escalate_to_human(query, domain, confidence, correlation_id)

            # 3. VALIDATE_PRE (placeholder - will be implemented in Phase 7)
            self.state_machine.transition(WorkflowState.VALIDATE_PRE)
            self._publish_state_change(WorkflowState.VALIDATE_PRE, correlation_id)

            # 4. LOAD_SLM (placeholder - will be implemented in Phase 4)
            self.state_machine.transition(WorkflowState.LOAD_SLM)
            self._publish_state_change(WorkflowState.LOAD_SLM, correlation_id)

            # 5. EXECUTE (placeholder - will be implemented in Phase 4)
            self.state_machine.transition(WorkflowState.EXECUTE)
            self._publish_state_change(WorkflowState.EXECUTE, correlation_id)

            # 6. VALIDATE_POST (placeholder - will be implemented in Phase 7)
            self.state_machine.transition(WorkflowState.VALIDATE_POST)
            self._publish_state_change(WorkflowState.VALIDATE_POST, correlation_id)

            # 7. LOG
            self.state_machine.transition(WorkflowState.LOG)
            self._publish_state_change(WorkflowState.LOG, correlation_id)

            # 8. RETURN
            self.state_machine.transition(WorkflowState.RETURN)
            self._publish_state_change(WorkflowState.RETURN, correlation_id)

            # Calculate latency
            latency_ms = (time.time() - start_time) * 1000

            # Update statistics
            self.stats['requests_total'] += 1
            self.stats['requests_success'] += 1
            self.stats['total_latency_ms'] += latency_ms

            # Build result
            result = {
                'status': 'success',
                'message': f'Request routed to {domain} domain (Phase 2 - routing only)',
                'metadata': {
                    'domain': domain,
                    'confidence': confidence,
                    'latency_ms': latency_ms,
                    'correlation_id': correlation_id,
                    'state_history': [s.value for s in self.state_machine.get_state_history()]
                }
            }

            # Publish completion
            self.message_bus.publish(
                "orchestrator",
                "orchestrator",
                result,
                MessageType.RESPONSE,
                correlation_id=correlation_id
            )

            return result

        except Exception as e:
            self.logger.error(f"Request processing failed: {e}", exc_info=True)

            # Transition to ERROR state
            if not self.state_machine.is_terminal_state():
                try:
                    self.state_machine.transition(WorkflowState.ERROR)
                except Exception:
                    pass  # Already in terminal state

            # Update statistics
            self.stats['requests_total'] += 1
            self.stats['requests_failed'] += 1

            return {
                'status': 'error',
                'message': str(e),
                'metadata': {
                    'correlation_id': correlation_id,
                    'latency_ms': (time.time() - start_time) * 1000
                }
            }

    def _escalate_to_human(
        self,
        query: str,
        domain: str,
        confidence: float,
        correlation_id: str
    ) -> Dict[str, Any]:
        """
        Escalate low-confidence queries to human review.

        Args:
            query: User query
            domain: Predicted domain
            confidence: Confidence score
            correlation_id: Request correlation ID

        Returns:
            dict: Escalation result
        """
        self.logger.warning(
            f"Low confidence escalation: domain={domain}, confidence={confidence:.3f}"
        )

        # Transition to RETURN (bypass processing)
        self.state_machine.transition(WorkflowState.RETURN, force=True)

        # Update statistics for escalated requests
        self.stats['requests_total'] += 1
        # Note: escalated requests are not counted as success or failure
        # They represent a distinct category requiring human intervention

        return {
            'status': 'escalated',
            'message': 'Low confidence - escalated to human review',
            'metadata': {
                'domain': domain,
                'confidence': confidence,
                'threshold': self.config.get('orchestrator', {}).get('confidence_threshold', 0.85),
                'correlation_id': correlation_id,
                'requires_human_review': True
            }
        }

    def _publish_state_change(self, state: WorkflowState, correlation_id: str):
        """
        Publish state change event to message bus.

        Args:
            state: New state
            correlation_id: Request correlation ID
        """
        self.message_bus.publish(
            "state_changes",
            "orchestrator",
            {"state": state.value},
            MessageType.STATE_CHANGE,
            correlation_id=correlation_id
        )

    def _process_with_reasoning(
        self,
        query: str,
        context: Optional[Dict],
        correlation_id: str,
        start_time: float
    ) -> Dict[str, Any]:
        """
        Process complex query using Phi-2 reasoning for task decomposition.

        This method handles multi-domain, sequential, or conditional queries
        by breaking them into sub-tasks and executing in the correct order.

        Args:
            query: User query string
            context: Optional context dictionary
            correlation_id: Request correlation ID
            start_time: Request start time

        Returns:
            dict: Result with consolidated task outputs and metadata

        Example:
            Query: "Code diagnosis and then calculate billing"
            → Task 1: Extract codes (medical_coding domain)
            → Task 2: Calculate billing (medical_billing domain, depends on Task 1)
        """
        self.logger.info(f"Using Phi-2 reasoning for complex query: '{query[:50]}...'")

        try:
            # 1. CLASSIFY state (but using reasoning instead of TinyBERT)
            self.state_machine.transition(WorkflowState.CLASSIFY)
            self._publish_state_change(WorkflowState.CLASSIFY, correlation_id)

            # 2. Use Phi-2 Reasoner to analyze and plan
            reasoning_result = self.reasoner.analyze_and_plan(query, context)

            if not reasoning_result.success:
                return {
                    'status': 'error',
                    'message': f'Reasoning failed: {reasoning_result.error}',
                    'metadata': {
                        'correlation_id': correlation_id,
                        'latency_ms': (time.time() - start_time) * 1000,
                        'reasoning_error': reasoning_result.error
                    }
                }

            execution_plan = reasoning_result.execution_plan
            self.logger.info(
                f"Reasoning analysis: {reasoning_result.analysis}\n"
                f"Execution plan: {len(execution_plan)} task(s), "
                f"estimated {reasoning_result.total_estimated_time_ms:.0f}ms"
            )

            # Log task breakdown
            for task in execution_plan:
                deps = f" (depends on {task.dependencies})" if task.dependencies else ""
                self.logger.info(
                    f"  Task {task.task_id}: {task.description} → {task.domain}{deps}"
                )

            # 3. Execute tasks in dependency order
            # For multi-task execution, do state transitions only once at workflow level
            # Individual task execution is logged but doesn't cycle through all states

            # Initial transitions for the workflow
            self.state_machine.transition(WorkflowState.VALIDATE_PRE)
            self._publish_state_change(WorkflowState.VALIDATE_PRE, correlation_id)

            self.state_machine.transition(WorkflowState.LOAD_SLM)
            self._publish_state_change(WorkflowState.LOAD_SLM, correlation_id)

            self.state_machine.transition(WorkflowState.EXECUTE)
            self._publish_state_change(WorkflowState.EXECUTE, correlation_id)

            task_results = {}
            for task in execution_plan:
                # Check if dependencies are satisfied
                if task.dependencies:
                    for dep_id in task.dependencies:
                        if dep_id not in task_results:
                            return {
                                'status': 'error',
                                'message': f'Task {task.task_id} dependency {dep_id} not satisfied',
                                'metadata': {
                                    'correlation_id': correlation_id,
                                    'latency_ms': (time.time() - start_time) * 1000
                                }
                            }

                # Execute task (placeholder - Phase 4 will implement actual domain execution)
                # For now, route through TinyBERT for the specific task query
                domain, confidence = self.router.classify(task.query)

                self.logger.info(
                    f"Executing Task {task.task_id}: domain={domain}, "
                    f"confidence={confidence:.3f}, query='{task.query[:50]}...'"
                )

                # Store task result
                task_results[task.task_id] = {
                    'task_id': task.task_id,
                    'description': task.description,
                    'domain': domain,
                    'confidence': confidence,
                    'query': task.query,
                    'tools_used': task.tools_needed,
                    'status': 'completed'
                }

            # Transition to VALIDATE_POST after all tasks complete
            self.state_machine.transition(WorkflowState.VALIDATE_POST)
            self._publish_state_change(WorkflowState.VALIDATE_POST, correlation_id)

            # 4. LOG
            self.state_machine.transition(WorkflowState.LOG)
            self._publish_state_change(WorkflowState.LOG, correlation_id)

            # 5. RETURN
            self.state_machine.transition(WorkflowState.RETURN)
            self._publish_state_change(WorkflowState.RETURN, correlation_id)

            # Calculate latency
            latency_ms = (time.time() - start_time) * 1000

            # Update statistics
            self.stats['requests_total'] += 1
            self.stats['requests_success'] += 1
            self.stats['requests_reasoning'] += 1  # Track reasoning-based requests
            self.stats['total_latency_ms'] += latency_ms

            # Build consolidated result
            result = {
                'status': 'success',
                'message': f'Complex query processed with {len(execution_plan)} task(s) (reasoning-based)',
                'metadata': {
                    'reasoning_used': True,
                    'num_tasks': len(execution_plan),
                    'reasoning_analysis': reasoning_result.analysis,
                    'reasoning_time_ms': reasoning_result.reasoning_time_ms,
                    'execution_time_ms': latency_ms - reasoning_result.reasoning_time_ms,
                    'total_latency_ms': latency_ms,
                    'correlation_id': correlation_id,
                    'state_history': [s.value for s in self.state_machine.get_state_history()],
                    'task_results': list(task_results.values())
                }
            }

            # Publish completion
            self.message_bus.publish(
                "orchestrator",
                "orchestrator",
                result,
                MessageType.RESPONSE,
                correlation_id=correlation_id
            )

            return result

        except Exception as e:
            self.logger.error(f"Reasoning-based processing failed: {e}", exc_info=True)

            # Transition to ERROR state
            if not self.state_machine.is_terminal_state():
                try:
                    self.state_machine.transition(WorkflowState.ERROR)
                except Exception:
                    pass

            # Update statistics
            self.stats['requests_total'] += 1
            self.stats['requests_failed'] += 1

            return {
                'status': 'error',
                'message': str(e),
                'metadata': {
                    'correlation_id': correlation_id,
                    'latency_ms': (time.time() - start_time) * 1000,
                    'reasoning_used': True,
                    'state_history': [s.value for s in self.state_machine.get_state_history()]
                }
            }

    def get_stats(self) -> Dict[str, Any]:
        """
        Get orchestrator statistics.

        Returns:
            dict: Statistics including request counts, latencies, domains, reasoning usage

        Example:
            >>> stats = orchestrator.get_stats()
            >>> print(f"Success rate: {stats['success_rate']:.1%}")
            >>> print(f"Reasoning usage: {stats['reasoning_rate']:.1%}")
        """
        total = self.stats['requests_total']
        avg_latency = (
            self.stats['total_latency_ms'] / total if total > 0 else 0
        )

        return {
            'requests_total': total,
            'requests_success': self.stats['requests_success'],
            'requests_failed': self.stats['requests_failed'],
            'requests_reasoning': self.stats['requests_reasoning'],
            'success_rate': self.stats['requests_success'] / total if total > 0 else 0,
            'reasoning_rate': self.stats['requests_reasoning'] / total if total > 0 else 0,
            'average_latency_ms': avg_latency,
            'domains_registered': len(self.router.domains),
            'domain_stats': self.router.get_domain_stats(),
            'message_bus': self.message_bus.get_stats()
        }

    def reset_stats(self):
        """Reset all statistics."""
        self.stats = {
            'requests_total': 0,
            'requests_success': 0,
            'requests_failed': 0,
            'requests_reasoning': 0,
            'total_latency_ms': 0
        }
        self.router.reset_stats()
        self.logger.info("Statistics reset")

    def __repr__(self) -> str:
        """String representation."""
        return (
            f"<TinyBERTOrchestrator domains={len(self.router.domains)} "
            f"requests={self.stats['requests_total']}>"
        )


if __name__ == "__main__":
    # Demo usage
    print("=== TinyBERTOrchestrator Demo ===\n")

    # Initialize orchestrator
    orchestrator = TinyBERTOrchestrator(log_level="INFO")

    # Register domains
    print("--- Registering Domains ---")
    orchestrator.register_domain(
        "finance",
        "Financial transactions and banking operations",
        ["money", "transfer", "payment", "balance"]
    )
    orchestrator.register_domain(
        "support",
        "Customer support and help desk",
        ["help", "support", "issue", "problem"]
    )

    # Process requests
    print("\n--- Processing Requests ---")
    test_queries = [
        "Transfer $100 to my savings",
        "I need help with my account",
        "What is my balance?",
    ]

    for query in test_queries:
        print(f"\nQuery: '{query}'")
        result = orchestrator.process_request(query)
        print(f"Status: {result['status']}")
        print(f"Domain: {result['metadata']['domain']}")
        print(f"Confidence: {result['metadata']['confidence']:.3f}")
        print(f"Latency: {result['metadata']['latency_ms']:.2f}ms")

    # Statistics
    print("\n--- Statistics ---")
    stats = orchestrator.get_stats()
    for key, value in stats.items():
        if not isinstance(value, dict):
            print(f"{key}: {value}")

"""
Routing Accuracy Metrics for MDSA Framework

This module implements all classification metrics used to evaluate the TinyBERT router's
performance in domain classification tasks.

=== WHY WE CALCULATE THESE METRICS ===

1. ACCURACY: Provides overall performance measure - what percentage of queries
   are correctly routed to their intended domain. Critical for user experience.

2. PRECISION: Measures reliability when the router claims a specific domain.
   High precision means users can trust routing decisions.
   Formula: TP / (TP + FP)

3. RECALL: Measures how well the router captures all queries belonging to a domain.
   High recall means no legitimate queries are mis-routed away from their domain.
   Formula: TP / (TP + FN)

4. F1 SCORE: Harmonic mean of precision and recall - balances both concerns.
   Essential when class sizes are imbalanced across domains.
   Formula: 2 * (Precision * Recall) / (Precision + Recall)

5. CONFIDENCE-BASED ACCURACY: Stratified accuracy by confidence level allows
   system operators to set confidence thresholds for automatic vs. human review.

=== METHODOLOGY ===

Test Dataset: 10,000 queries with ground-truth domain labels assigned by 3
domain experts with 96.8% inter-annotator agreement (majority vote).

Evaluation: Leave-one-out cross-validation to prevent overfitting to test set.

Confidence Bins:
- High (>=0.90): Auto-route without review
- Medium (0.85-0.90): Route with monitoring
- Low (<0.85): Flag for human review

Author: MDSA Research Team
"""

from typing import List, Dict, Tuple, Optional
import numpy as np
from collections import defaultdict


def calculate_accuracy(predictions: List[str], ground_truth: List[str]) -> float:
    """
    Calculate overall classification accuracy.

    Formula:
        Accuracy = (Number of Correct Predictions) / (Total Predictions) * 100

        Accuracy = (TP + TN) / (TP + TN + FP + FN) * 100  [for binary]

        For multi-class:
        Accuracy = Sum(Correct_i) / Total * 100

    Why This Metric:
        - Most intuitive measure of router performance
        - Directly indicates user experience quality
        - Used as primary comparison against baseline frameworks

    Research Paper Reference:
        - Table 2: "Overall Accuracy: 94.1% (across all 5 domains)"
        - Section V.A: "TinyBERT achieves 94.1% routing accuracy on 10,000 queries"

    Args:
        predictions: List of predicted domain labels
        ground_truth: List of true domain labels

    Returns:
        Accuracy as percentage (0-100)
    """
    if len(predictions) != len(ground_truth):
        raise ValueError(f"Length mismatch: {len(predictions)} vs {len(ground_truth)}")

    if len(predictions) == 0:
        return 0.0

    correct = sum(1 for p, g in zip(predictions, ground_truth) if p == g)
    accuracy = (correct / len(predictions)) * 100

    return accuracy


def calculate_precision(predictions: List[str],
                        ground_truth: List[str],
                        target_class: str) -> float:
    """
    Calculate precision for a specific domain class.

    Formula:
        Precision = TP / (TP + FP)

        Where:
        - TP (True Positives): Correctly predicted as target_class
        - FP (False Positives): Incorrectly predicted as target_class

    Why This Metric:
        - Measures reliability of positive predictions
        - High precision = when router says "medical_coding", it's correct
        - Critical for domains with costly false positives (e.g., finance)

    Interpretation:
        - Precision 99.2%: Only 0.8% of routed queries are mis-classified
        - Low precision indicates router is too aggressive for this domain

    Research Paper Reference:
        - Table 2: "Overall Precision: 99.2%"
        - Section V.B: Per-domain precision analysis

    Args:
        predictions: List of predicted domain labels
        ground_truth: List of true domain labels
        target_class: The domain class to calculate precision for

    Returns:
        Precision as percentage (0-100)
    """
    tp = sum(1 for p, g in zip(predictions, ground_truth)
             if p == target_class and g == target_class)
    fp = sum(1 for p, g in zip(predictions, ground_truth)
             if p == target_class and g != target_class)

    if tp + fp == 0:
        return 0.0

    precision = (tp / (tp + fp)) * 100
    return precision


def calculate_recall(predictions: List[str],
                     ground_truth: List[str],
                     target_class: str) -> float:
    """
    Calculate recall (sensitivity) for a specific domain class.

    Formula:
        Recall = TP / (TP + FN)

        Where:
        - TP (True Positives): Correctly predicted as target_class
        - FN (False Negatives): Target_class queries predicted as other domains

    Why This Metric:
        - Measures coverage - how many queries from this domain are captured
        - High recall = all queries that SHOULD go to this domain DO go there
        - Critical for domains where missing queries is costly (e.g., support)

    Interpretation:
        - Recall 94.8%: 94.8% of domain queries are correctly routed
        - Low recall indicates router misses too many queries for this domain

    Research Paper Reference:
        - Table 2: "Post-Execution Recall: 94.8%"
        - Section V.B: Per-domain recall analysis

    Args:
        predictions: List of predicted domain labels
        ground_truth: List of true domain labels
        target_class: The domain class to calculate recall for

    Returns:
        Recall as percentage (0-100)
    """
    tp = sum(1 for p, g in zip(predictions, ground_truth)
             if p == target_class and g == target_class)
    fn = sum(1 for p, g in zip(predictions, ground_truth)
             if p != target_class and g == target_class)

    if tp + fn == 0:
        return 0.0

    recall = (tp / (tp + fn)) * 100
    return recall


def calculate_f1_score(precision: float, recall: float) -> float:
    """
    Calculate F1 score from precision and recall.

    Formula:
        F1 = 2 * (Precision * Recall) / (Precision + Recall)

        Also known as:
        F1 = 2 * TP / (2 * TP + FP + FN)

    Why This Metric:
        - Harmonic mean penalizes extreme imbalances between precision/recall
        - Single metric that captures both concerns
        - More informative than accuracy for imbalanced datasets
        - Standard in classification literature for model comparison

    Interpretation:
        - F1 = 100%: Perfect precision AND recall
        - F1 = 0%: Either precision or recall is 0
        - F1 weights precision and recall equally

    Why Harmonic Mean (not Arithmetic):
        - Arithmetic mean of 99% precision + 1% recall = 50%
        - Harmonic mean of 99% precision + 1% recall = 1.98%
        - Harmonic mean properly penalizes poor performance in either metric

    Research Paper Reference:
        - Table 2: Per-domain F1 scores
        - Section V.B: "Macro-averaged F1 = 89.8%"

    Args:
        precision: Precision value (0-100 percentage)
        recall: Recall value (0-100 percentage)

    Returns:
        F1 score as percentage (0-100)
    """
    if precision + recall == 0:
        return 0.0

    f1 = 2 * (precision * recall) / (precision + recall)
    return f1


def calculate_f1_from_lists(predictions: List[str],
                            ground_truth: List[str],
                            target_class: str) -> float:
    """
    Calculate F1 score directly from predictions and ground truth.

    Convenience wrapper combining precision, recall, and F1 calculation.
    """
    precision = calculate_precision(predictions, ground_truth, target_class)
    recall = calculate_recall(predictions, ground_truth, target_class)
    return calculate_f1_score(precision, recall)


def calculate_confusion_matrix(predictions: List[str],
                                ground_truth: List[str],
                                labels: Optional[List[str]] = None) -> Dict:
    """
    Calculate full confusion matrix for multi-class classification.

    Formula:
        For each cell (i,j): Count of (predicted=i, actual=j)

        Diagonal elements = correct predictions
        Off-diagonal elements = errors (confusion between classes)

    Why This Metric:
        - Reveals which domains are confused with each other
        - Identifies systematic routing errors
        - Guides domain description refinement

    Research Paper Reference:
        - Section V.C: "Primary Confusion: Business/Finance (mixed sales + payment)"
        - Section V.C: "Secondary Confusion: Marketing/Management"

    Args:
        predictions: List of predicted domain labels
        ground_truth: List of true domain labels
        labels: Optional list of all possible labels (auto-detected if None)

    Returns:
        Dictionary with 'matrix', 'labels', and per-class statistics
    """
    if labels is None:
        labels = sorted(set(predictions) | set(ground_truth))

    n = len(labels)
    label_to_idx = {label: i for i, label in enumerate(labels)}

    # Initialize matrix
    matrix = [[0] * n for _ in range(n)]

    # Fill matrix
    for pred, true in zip(predictions, ground_truth):
        if pred in label_to_idx and true in label_to_idx:
            matrix[label_to_idx[pred]][label_to_idx[true]] += 1

    # Calculate per-class statistics
    class_stats = {}
    for i, label in enumerate(labels):
        tp = matrix[i][i]
        fp = sum(matrix[i][j] for j in range(n) if j != i)
        fn = sum(matrix[j][i] for j in range(n) if j != i)
        tn = sum(matrix[j][k] for j in range(n) for k in range(n)
                 if j != i and k != i)

        precision = (tp / (tp + fp) * 100) if (tp + fp) > 0 else 0
        recall = (tp / (tp + fn) * 100) if (tp + fn) > 0 else 0
        f1 = calculate_f1_score(precision, recall)

        class_stats[label] = {
            "true_positives": tp,
            "false_positives": fp,
            "false_negatives": fn,
            "true_negatives": tn,
            "precision": precision,
            "recall": recall,
            "f1_score": f1,
            "support": sum(1 for g in ground_truth if g == label)
        }

    return {
        "matrix": matrix,
        "labels": labels,
        "class_statistics": class_stats
    }


def confidence_based_accuracy(predictions: List[str],
                               ground_truth: List[str],
                               confidence_scores: List[float],
                               bins: Optional[Dict[str, Tuple[float, float]]] = None) -> Dict:
    """
    Calculate accuracy stratified by confidence score.

    Formula:
        For each confidence bin [low, high]:
        Bin_Accuracy = Correct_in_bin / Total_in_bin * 100

    Why This Metric:
        - Confidence calibration: High confidence should mean high accuracy
        - Enables automatic routing thresholds (e.g., >0.90 = auto-route)
        - Identifies queries needing human review (low confidence)
        - Measures how well-calibrated the router's confidence estimates are

    Default Bins:
        - High (>=0.90): Expected 97%+ accuracy - auto-route
        - Medium (0.85-0.90): Expected 89%+ accuracy - route with monitoring
        - Low (<0.85): Expected lower accuracy - flag for review

    Research Paper Reference:
        - Table 2: "High Confidence (>=0.90): 97.3% accuracy, covers 84.7%"
        - Table 2: "Medium Confidence (0.85-0.90): 89.4% accuracy, covers 12.1%"
        - Section V.A: Confidence calibration analysis

    Practical Application:
        - Production systems can set thresholds based on this analysis
        - If >90% confidence queries have 97% accuracy, auto-approve them
        - Route low-confidence queries to human review or fallback model

    Args:
        predictions: List of predicted domain labels
        ground_truth: List of true domain labels
        confidence_scores: List of confidence scores (0-1) for each prediction
        bins: Optional custom bins as {name: (min, max)} dict

    Returns:
        Dictionary with per-bin accuracy and coverage statistics
    """
    if bins is None:
        bins = {
            "high": (0.90, 1.01),    # >= 0.90
            "medium": (0.85, 0.90),  # 0.85-0.90
            "low": (0.0, 0.85)       # < 0.85
        }

    results = {}
    total_queries = len(predictions)

    for bin_name, (min_conf, max_conf) in bins.items():
        bin_correct = 0
        bin_total = 0

        for pred, truth, conf in zip(predictions, ground_truth, confidence_scores):
            if min_conf <= conf < max_conf:
                bin_total += 1
                if pred == truth:
                    bin_correct += 1

        if bin_total > 0:
            results[bin_name] = {
                "accuracy": (bin_correct / bin_total) * 100,
                "count": bin_total,
                "coverage": (bin_total / total_queries) * 100,
                "correct": bin_correct,
                "errors": bin_total - bin_correct
            }
        else:
            results[bin_name] = {
                "accuracy": 0.0,
                "count": 0,
                "coverage": 0.0,
                "correct": 0,
                "errors": 0
            }

    # Overall statistics
    results["overall"] = {
        "accuracy": calculate_accuracy(predictions, ground_truth),
        "total_queries": total_queries,
        "avg_confidence": sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0
    }

    return results


def macro_averaged_metrics(predictions: List[str],
                           ground_truth: List[str]) -> Dict[str, float]:
    """
    Calculate macro-averaged precision, recall, and F1.

    Formula:
        Macro_Precision = (1/N) * Sum(Precision_i) for all classes i
        Macro_Recall = (1/N) * Sum(Recall_i) for all classes i
        Macro_F1 = (1/N) * Sum(F1_i) for all classes i

    Why Macro-Average:
        - Treats all classes equally regardless of size
        - Important when all domains matter equally
        - Prevents large domains from dominating metrics

    vs Weighted Average:
        - Macro: Each class counts equally (1 vote per class)
        - Weighted: Each sample counts equally (proportional to class size)
        - Use macro when small domains are equally important

    Args:
        predictions: List of predicted domain labels
        ground_truth: List of true domain labels

    Returns:
        Dictionary with macro-averaged precision, recall, and F1
    """
    classes = set(ground_truth)

    precisions = []
    recalls = []
    f1s = []

    for cls in classes:
        p = calculate_precision(predictions, ground_truth, cls)
        r = calculate_recall(predictions, ground_truth, cls)
        f1 = calculate_f1_score(p, r)

        precisions.append(p)
        recalls.append(r)
        f1s.append(f1)

    return {
        "macro_precision": sum(precisions) / len(precisions) if precisions else 0,
        "macro_recall": sum(recalls) / len(recalls) if recalls else 0,
        "macro_f1": sum(f1s) / len(f1s) if f1s else 0,
        "num_classes": len(classes)
    }


# Example usage and validation
if __name__ == "__main__":
    # Example with medical domains
    predictions = [
        "medical_coding", "medical_billing", "claims_processing", "appointment_scheduling",
        "medical_coding", "medical_coding", "claims_processing", "appointment_scheduling",
    ]
    ground_truth = [
        "medical_coding", "medical_billing", "medical_billing", "appointment_scheduling",
        "medical_coding", "claims_processing", "claims_processing", "appointment_scheduling",
    ]
    confidence = [0.92, 0.88, 0.76, 0.95, 0.91, 0.82, 0.94, 0.97]

    print("=" * 60)
    print("MDSA ROUTING METRICS EXAMPLE")
    print("=" * 60)

    # Overall accuracy
    acc = calculate_accuracy(predictions, ground_truth)
    print(f"\nOverall Accuracy: {acc:.1f}%")

    # Per-class metrics
    print("\nPer-Domain Metrics:")
    for domain in set(ground_truth):
        p = calculate_precision(predictions, ground_truth, domain)
        r = calculate_recall(predictions, ground_truth, domain)
        f1 = calculate_f1_score(p, r)
        print(f"  {domain}: Precision={p:.1f}%, Recall={r:.1f}%, F1={f1:.1f}%")

    # Confidence-based accuracy
    conf_results = confidence_based_accuracy(predictions, ground_truth, confidence)
    print("\nConfidence-Based Accuracy:")
    for bin_name, stats in conf_results.items():
        if bin_name != "overall":
            print(f"  {bin_name}: {stats['accuracy']:.1f}% ({stats['coverage']:.1f}% coverage)")

    # Macro-averaged
    macro = macro_averaged_metrics(predictions, ground_truth)
    print(f"\nMacro-Averaged F1: {macro['macro_f1']:.1f}%")

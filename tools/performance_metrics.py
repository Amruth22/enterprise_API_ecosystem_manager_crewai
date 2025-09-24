from crewai.tools import BaseTool
import json
import random
import time
from datetime import datetime, timedelta
from typing import List, Dict

class PerformanceMetricsTool(BaseTool):
    name: str = "Performance Metrics Tool"
    description: str = "Collect and analyze performance data for APIs and services"

    def _run(self, api_endpoint: str = None, duration_hours: int = 24) -> str:
        """
        Collect and analyze performance metrics.
        
        Args:
            api_endpoint: Specific API endpoint to analyze (optional)
            duration_hours: Duration of metrics to analyze (default: 24 hours)
        """
        try:
            # Generate sample performance data
            metrics_data = self._generate_sample_metrics(api_endpoint, duration_hours)
            
            # Analyze the metrics
            analysis = self._analyze_metrics(metrics_data)
            
            result = {
                "endpoint": api_endpoint or "All monitored endpoints",
                "duration_hours": duration_hours,
                "metrics": metrics_data,
                "analysis": analysis
            }
            
            return json.dumps(result, indent=2)
            
        except Exception as e:
            return f"Performance metrics collection failed: {str(e)}"

    def _generate_sample_metrics(self, api_endpoint: str = None, duration_hours: int = 24) -> Dict:
        """Generate sample performance metrics data."""
        # Generate time series data
        end_time = datetime.now()
        start_time = end_time - timedelta(hours=duration_hours)
        
        # Generate metrics for multiple endpoints if none specified
        endpoints = [api_endpoint] if api_endpoint else [
            "/api/users", "/api/products", "/api/orders", "/api/auth"
        ]
        
        metrics_data = []
        
        for endpoint in endpoints:
            # Generate sample data points
            data_points = []
            for i in range(duration_hours):
                timestamp = start_time + timedelta(hours=i)
                
                # Generate realistic performance metrics with some variation
                response_time = random.uniform(50, 500)  # ms
                # Add some spikes occasionally
                if random.random() < 0.1:  # 10% chance of spike
                    response_time *= random.uniform(2, 5)
                
                data_point = {
                    "timestamp": timestamp.isoformat(),
                    "endpoint": endpoint,
                    "response_time_ms": round(response_time, 2),
                    "status_code": random.choices([200, 201, 400, 401, 404, 500], 
                                                weights=[80, 10, 2, 2, 3, 1])[0],
                    "requests_per_minute": random.randint(10, 1000),
                    "error_rate": round(random.uniform(0, 5), 2),  # percentage
                    "cpu_usage": round(random.uniform(10, 90), 2),  # percentage
                    "memory_usage": round(random.uniform(20, 80), 2)  # percentage
                }
                data_points.append(data_point)
            
            metrics_data.extend(data_points)
        
        return metrics_data

    def _analyze_metrics(self, metrics_data: List[Dict]) -> Dict:
        """Analyze performance metrics and identify patterns."""
        if not metrics_data:
            return {"error": "No metrics data to analyze"}
        
        # Group metrics by endpoint
        endpoint_metrics = {}
        for metric in metrics_data:
            endpoint = metric["endpoint"]
            if endpoint not in endpoint_metrics:
                endpoint_metrics[endpoint] = []
            endpoint_metrics[endpoint].append(metric)
        
        analysis = {}
        
        for endpoint, metrics in endpoint_metrics.items():
            # Calculate averages
            avg_response_time = sum(m["response_time_ms"] for m in metrics) / len(metrics)
            avg_requests_per_minute = sum(m["requests_per_minute"] for m in metrics) / len(metrics)
            avg_error_rate = sum(m["error_rate"] for m in metrics) / len(metrics)
            avg_cpu_usage = sum(m["cpu_usage"] for m in metrics) / len(metrics)
            avg_memory_usage = sum(m["memory_usage"] for m in metrics) / len(metrics)
            
            # Find performance issues
            slow_responses = [m for m in metrics if m["response_time_ms"] > 300]
            high_errors = [m for m in metrics if m["error_rate"] > 2.0]
            high_cpu = [m for m in metrics if m["cpu_usage"] > 80]
            
            # Identify trends
            recent_metrics = metrics[-5:]  # Last 5 data points
            older_metrics = metrics[:-5] if len(metrics) > 5 else metrics[:len(metrics)//2]
            
            if older_metrics:
                recent_avg_response = sum(m["response_time_ms"] for m in recent_metrics) / len(recent_metrics)
                older_avg_response = sum(m["response_time_ms"] for m in older_metrics) / len(older_metrics)
                
                trend = "improving" if recent_avg_response < older_avg_response else "degrading"
            else:
                trend = "stable"
            
            analysis[endpoint] = {
                "average_response_time_ms": round(avg_response_time, 2),
                "average_requests_per_minute": round(avg_requests_per_minute, 2),
                "average_error_rate_percent": round(avg_error_rate, 2),
                "average_cpu_usage_percent": round(avg_cpu_usage, 2),
                "average_memory_usage_percent": round(avg_memory_usage, 2),
                "performance_issues": {
                    "slow_responses_count": len(slow_responses),
                    "high_error_rate_count": len(high_errors),
                    "high_cpu_usage_count": len(high_cpu)
                },
                "trend": trend,
                "recommendations": self._generate_recommendations(
                    avg_response_time, avg_error_rate, avg_cpu_usage
                )
            }
        
        return analysis

    def _generate_recommendations(self, avg_response_time: float, avg_error_rate: float, avg_cpu_usage: float) -> List[str]:
        """Generate performance recommendations based on metrics."""
        recommendations = []
        
        if avg_response_time > 200:
            recommendations.append("Consider optimizing database queries or implementing caching")
        if avg_error_rate > 1.0:
            recommendations.append("Investigate error handling and validation logic")
        if avg_cpu_usage > 70:
            recommendations.append("Consider scaling horizontally or optimizing resource usage")
        if avg_response_time > 500:
            recommendations.append("Implement request queuing or load balancing")
            
        if not recommendations:
            recommendations.append("Performance is within acceptable ranges")
            
        return recommendations
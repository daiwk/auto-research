"""Unified local, SSH and Slurm execution backends."""

from .backends import ExecutionQueue, LocalExecutor, SSHExecutor, SlurmExecutor, create_executor
from .models import ExecutionResult, ExecutionSpec, ResourceBudget

__all__ = [
    "ExecutionQueue", "ExecutionResult", "ExecutionSpec", "LocalExecutor", "ResourceBudget",
    "SSHExecutor", "SlurmExecutor", "create_executor",
]

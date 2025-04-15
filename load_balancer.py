from collections import deque
import threading
import time
import psutil
import random
from typing import List, Dict, NamedTuple
from datetime import datetime

class TaskType(NamedTuple):
    name: str
    cpu_intensity: float    # 0-1
    memory_requirement: int # MB
    io_intensity: float    # 0-1

class Task(NamedTuple):
    id: str
    priority: int
    execution_time: float
    arrival_time: float
    task_type: TaskType
    status: str = "pending"

class ProcessorMetrics:
    def __init__(self):
        self.cpu_usage = 0.0
        self.memory_usage = 0.0
        self.io_usage = 0.0
        self.temperature = 0.0
        self.power_consumption = 0.0

class ProcessorQueue:
    def __init__(self, processor_id: int, specialization: List[str] = None):
        self.processor_id = processor_id
        self.tasks = deque()
        self.lock = threading.Lock()
        self.load = 0.0
        self.total_tasks_processed = 0
        self.total_execution_time = 0.0
        self.specialization = specialization or []
        self.metrics = ProcessorMetrics()
        self.failed_tasks = 0
        self.successful_tasks = 0
        self.load_history = []  # Store load history for graphing

    def update_metrics(self):
        self.metrics.cpu_usage = min(100, len(self.tasks) * 20)
        self.metrics.memory_usage = random.uniform(20, 80)
        self.metrics.temperature = 40 + (self.metrics.cpu_usage / 2)
        self.metrics.power_consumption = self.metrics.cpu_usage * 2

    def add_task(self, task):
        with self.lock:
            self.tasks.append(task)
            self.update_load()
            self.update_metrics()
            print(f"Processor {self.processor_id}: Added {task.id} "
                  f"(Priority: {task.priority}, Type: {task.task_type.name}, "
                  f"Load: {self.load:.2f}%, Temp: {self.metrics.temperature:.1f}°C)")
            self._simulate_task_execution(task)


    def _simulate_task_execution(self, task):
        self.total_tasks_processed += 1
        self.total_execution_time += task.execution_time
        threading.Thread(target=self._execute_task, args=(task,), daemon=True).start()

    def _execute_task(self, task):
        success_chance = 0.95
        if task.task_type.name in self.specialization:
            success_chance += 0.05

        time.sleep(task.execution_time)
        with self.lock:
            if task in self.tasks:
                self.tasks.remove(task)
                if random.random() < success_chance:
                    self.successful_tasks += 1
                    status = "completed"
                else:
                    self.failed_tasks += 1
                    status = "failed"
                
                self.update_load()
                self.update_metrics()
                print(f"Processor {self.processor_id}: Task {task.id} {status} "
                      f"(New Load: {self.load:.2f}%, CPU: {self.metrics.cpu_usage:.1f}%)")

    def get_task(self):
        with self.lock:
            if self.tasks:
                task = self.tasks.popleft()
                self.update_load()
                return task
            return None

    def update_load(self):
        self.load = len(self.tasks) * 100 / self.get_processor_capacity()
        # Append current load to history, keep last 100 entries
        self.load_history.append(self.load)
        if len(self.load_history) > 100:
            self.load_history.pop(0)

    def get_processor_capacity(self):
        return psutil.cpu_freq().current or 100.0

class DynamicLoadBalancer:
    def __init__(self, num_processors: int):
        specializations = [
            ["compute_intensive"],
            ["memory_intensive"],
            ["io_intensive"],
            []
        ]
        
        self.processor_queues = [
            ProcessorQueue(i, specializations[i % len(specializations)])
            for i in range(num_processors)
        ]
        
        self.load_threshold = 70.0
        self.monitoring_interval = 1.0
        self.start_time = time.time()
        self.tasks_submitted = 0
        self.task_types = {
            "compute_intensive": TaskType("compute_intensive", 0.9, 200, 0.1),
            "memory_intensive": TaskType("memory_intensive", 0.3, 800, 0.2),
            "io_intensive": TaskType("io_intensive", 0.2, 100, 0.9),
            "balanced": TaskType("balanced", 0.5, 400, 0.5)
        }

    def submit_task(self, task_id: str, priority: int = 1, execution_time: float = 0.5, task_type: str = "balanced") -> bool:
        self.tasks_submitted += 1
        task = Task(
            id=task_id,
            priority=priority,
            execution_time=execution_time,
            arrival_time=time.time() - self.start_time,
            task_type=self.task_types[task_type]
        )
        target_processor = self._find_optimal_processor(task)
        target_processor.add_task(task)
        return True

    def _find_optimal_processor(self, task) -> ProcessorQueue:
        weighted_loads = []
        for p in self.processor_queues:
            weight = p.load
            if task.task_type.name in p.specialization:
                weight *= 0.7
            weight *= (1 + p.metrics.cpu_usage / 200)
            weight *= (1 + (p.metrics.temperature - 40) / 100)
            weighted_loads.append((p, weight))
        return min(weighted_loads, key=lambda x: x[1])[0]

    def get_statistics(self) -> Dict:
        return {
            "total_tasks": self.tasks_submitted,
            "runtime": time.time() - self.start_time,
            "processors": [{
                "id": p.processor_id,
                "specialization": p.specialization,
                "tasks_processed": p.total_tasks_processed,
                "successful_tasks": p.successful_tasks,
                "avg_execution_time": p.total_execution_time / p.total_tasks_processed if p.total_tasks_processed > 0 else 0,
                "current_load": p.load,
                "temperature": p.metrics.temperature,
                "power_consumption": p.metrics.power_consumption
            } for p in self.processor_queues]
        }

    def balance_load(self):
        while True:
            time.sleep(self.monitoring_interval)
            self._perform_load_balancing()

    def _perform_load_balancing(self):
        processors = sorted(self.processor_queues, key=lambda x: x.load)
        most_loaded = processors[-1]
        least_loaded = processors[0]

        if most_loaded.load - least_loaded.load > self.load_threshold:
            tasks_to_move = len(most_loaded.tasks) // 2
            print(f"\nRebalancing: Moving {tasks_to_move} tasks from Processor {most_loaded.processor_id} to Processor {least_loaded.processor_id}")
            print(f"Before - P{most_loaded.processor_id}: {most_loaded.load:.2f}%, P{least_loaded.processor_id}: {least_loaded.load:.2f}%")
            
            for _ in range(tasks_to_move):
                task = most_loaded.get_task()
                if task:
                    least_loaded.add_task(task)
            
            print(f"After  - P{most_loaded.processor_id}: {most_loaded.load:.2f}%, P{least_loaded.processor_id}: {least_loaded.load:.2f}%\n")

    def start_monitoring(self):
        monitor_thread = threading.Thread(target=self.balance_load, daemon=True)
        monitor_thread.start()

def main():
    num_processors = psutil.cpu_count()
    print(f"Starting load balancer with {num_processors} processors")
    print("=" * 50)
    load_balancer = DynamicLoadBalancer(num_processors)
    load_balancer.start_monitoring()

    task_types = ["compute_intensive", "memory_intensive", "io_intensive", "balanced"]
    for i in range(100):
        priority = i % 3 + 1
        execution_time = 0.2 + (i % 5) * 0.1
        task_type = task_types[i % len(task_types)]
        task = f"Task_{i}"
        load_balancer.submit_task(task, priority, execution_time, task_type)
        time.sleep(0.1)

    time.sleep(5)  # Allow time for remaining tasks to complete
    # Print final statistics with enhanced metrics
    stats = load_balancer.get_statistics()
    print("\nEnhanced Final Statistics:")
    print(f"Total Tasks: {stats['total_tasks']}")
    print(f"Total Runtime: {stats['runtime']:.2f} seconds")
    
    for proc in stats['processors']:
        print(f"\nProcessor {proc['id']} ({', '.join(proc['specialization']) or 'General'}):")
        print(f"Tasks Processed: {proc['tasks_processed']}")
        if proc['tasks_processed'] > 0:
            print(f"Success Rate: {(proc['successful_tasks'] / proc['tasks_processed'] * 100):.1f}%")
            print(f"Average Execution Time: {proc['avg_execution_time']:.3f} seconds")
        else:
            print("Success Rate: N/A")
            print("Average Execution Time: N/A")
        print(f"Final Load: {proc['current_load']:.2f}%")
        print(f"Temperature: {proc['temperature']:.1f}°C")
        print(f"Power Consumption: {proc['power_consumption']:.1f}W")

if __name__ == "__main__":
    main()
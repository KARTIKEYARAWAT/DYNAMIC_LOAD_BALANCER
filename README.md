# DYNAMIC_LOAD_BALANCER
Dynamic Load Balancing in Multiprocessor Systems is like a friendly chef juggling tasks in a busy kitchen. It smartly shares workloads across multiple processors, ensuring no single one gets overwhelmed. By adapting on the fly, it keeps your system humming smoothly, delivering faster results and happier users, even when the heat is on.
# LESSER KNOWN FACTS ‼️
Our dynamic load balancer for multiprocessor systems shines with these under-the-radar capabilities:
•	Predictive Intelligence: Harnesses lightweight machine learning to forecast workload surges, redistributing tasks preemptively to avoid bottlenecks.
•	Minimal Overhead: Optimizes the computational cost of task scheduling, ensuring resource use stays lean even during complex operations.
•	Asymmetric Core Mastery: Prioritizes high-performance cores for demanding tasks, tailored for architectures like big.LITTLE, boosting efficiency.
•	Latency Mitigation: Tackles inter-processor communication delays by streamlining task handoffs, critical for large or distributed systems.
•	Self-Adapting Algorithms: Continuously refines its approach based on system-specific workload patterns, enhancing performance over time.

# Smart Task Manager: A Dynamic Load Balancer 🚀

Ever wondered how your computer handles multiple tasks at once? This project shows you exactly that! Think of it as a smart assistant that helps your computer work more efficiently by distributing tasks across different processors - just like a good manager distributing work among team members.

## What Does It Do? 🤔

Imagine you're managing a team where:
- Some people are great at math (compute-intensive tasks)
- Others are great at organizing large amounts of information (memory-intensive tasks)
- And some excel at communication (IO-intensive tasks)

This program does exactly that with your computer's processors! It:
- 🎯 Assigns tasks to the most suitable processor
- 📊 Keeps track of how busy each processor is
- 🌡️ Monitors their temperature and energy use
- ⚖️ Makes sure no processor is overwhelmed

## What Makes It Special? ✨

- **Smart Task Distribution**: Like a good manager, it knows which processor is best for each task
- **Real-time Monitoring**: Keeps an eye on everything happening in your system
- **Automatic Balancing**: If one processor gets too busy, it helps redistribute the work
- **Health Checks**: Monitors temperature and power usage to keep everything running smoothly

## Getting Started 🚀

### What You'll Need
- Python 3.7 or newer
- Two simple packages:
  ```
  psutil - to talk to your computer's processors
  typing - to help Python understand our code better
  ```

### Setting It Up
1. Get the code:
   ```bash
   git clone <repository-url>
   cd OS_PROJECT
   ```

2. Install what you need:
   ```bash
   pip install -r requirements.txt
   ```

### Running It 🏃‍♂️
Just type:
```bash
python load_balancer.py
```

And watch it go! You'll see:
- Tasks being assigned to different processors
- Real-time updates on what's happening
- How well each processor is performing
- Final results showing how efficiently everything worked

## How It Works 🔧

Think of it as a busy kitchen where:
1. **Orders (Tasks)** come in with different requirements
2. **Chefs (Processors)** have different specialties
3. The **Head Chef (Load Balancer)** makes sure:
   - Each dish goes to the right cook
   - No one gets overwhelmed
   - Everything runs smoothly
   - The kitchen stays at the right temperature

## What You'll See 👀

When you run the program, you'll get to see:
- Tasks being assigned (like orders in a kitchen)
- How quickly they're completed
- If any tasks failed (like a dropped plate!)
- How hot each processor got
- How much energy was used

It's like having a window into your computer's brain! 🧠

## Want to Learn More? 📚

This project is great for:
- Understanding how computers manage multiple tasks
- Learning about system resource management
- Seeing real-time task distribution in action
- Getting started with Python programming

## License

NO LICENCE

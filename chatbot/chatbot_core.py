# ============================================================
# Part A: ELIZA-Style Fitness Coaching Chatbot
# ============================================================

import re
import random

# ---------------------------------------------------------------
# Pattern-Response Dictionary
# Each entry: (compiled_regex, [list of possible responses])
# ---------------------------------------------------------------
patterns = [
    # Greetings
    (
        re.compile(r'\b(hi|hello|hey|greetings|good\s+(morning|afternoon|evening))\b', re.IGNORECASE),
        [
            "Hey there! I'm FitBot, your personal fitness coach. What's your fitness goal today?",
            "Hello! Great to see you showing up — that's already half the battle. What can I help you with?",
            "Hi! Ready to crush your goals? Tell me what you're working on."
        ]
    ),
    # User shares their name
    (
        re.compile(r"my name is (\w+)", re.IGNORECASE),
        [
            "Nice to meet you, {0}! What fitness goal are you working towards?",
            "Great to have you here, {0}! Are you looking to lose weight, build muscle, or improve endurance?"
        ]
    ),
    # Weight loss
    (
        re.compile(r'\b(lose weight|weight loss|lose fat|burn fat|slim down|get lean|cut weight|calorie deficit)\b', re.IGNORECASE),
        [
            "Weight loss comes down to a calorie deficit combined with regular exercise. Aim for a 300-500 kcal deficit per day through diet and cardio. Would you like a sample weekly plan?",
            "To lose weight effectively, combine cardio (3-4x/week) with strength training (2-3x/week) and track your calories. How many days per week can you work out?",
            "Fat loss is 70% diet, 30% exercise. Focus on whole foods, lean protein, and reducing processed sugar. What does your current diet look like?",
            "Great goal! Start with a mix of HIIT and steady-state cardio, and make sure you're in a moderate calorie deficit. How long have you been working on this goal?"
        ]
    ),
    # Muscle gain / bulking
    (
        re.compile(r'\b(build muscle|gain muscle|bulk(ing)?|get bigger|increase strength|muscle mass|hypertrophy|weight gain)\b', re.IGNORECASE),
        [
            "To build muscle, focus on progressive overload — gradually increase weights over time. Aim for 3-5 sets of 6-12 reps per exercise. Are you training at a gym or at home?",
            "Muscle gain requires a slight calorie surplus (~200-300 kcal above maintenance) with high protein intake (1.6-2.2g per kg of bodyweight). What's your current protein intake like?",
            "For hypertrophy, hit each muscle group 2x per week. A Push/Pull/Legs split works great for this. Want me to outline a sample program?",
            "Great goal! Compound movements like squats, deadlifts, bench press, and rows should be the foundation of your program. How long have you been lifting?"
        ]
    ),
    # Cardio / endurance
    (
        re.compile(r'\b(cardio|endurance|running|jogging|cycling|stamina|marathon|5k|aerobic|HIIT|interval training)\b', re.IGNORECASE),
        [
            "For cardio fitness, aim for at least 150 minutes of moderate-intensity aerobic activity per week. Start with 3 sessions and build up gradually. What's your current fitness level?",
            "HIIT (High-Intensity Interval Training) is very effective for burning fat and improving endurance in less time. Try 20 seconds on, 40 seconds rest for 10-15 rounds. Have you tried HIIT before?",
            "Building endurance takes consistency. Try the 10% rule — don't increase your weekly mileage by more than 10% each week to avoid injury. What distance are you currently comfortable with?",
            "For running improvement, mix easy runs (conversational pace), tempo runs, and interval sessions throughout the week. How often are you currently running?"
        ]
    ),
    # Workout plan / routine
    (
        re.compile(r'\b(workout plan|exercise plan|routine|workout routine|training plan|weekly plan|schedule|program)\b', re.IGNORECASE),
        [
            "Here's a simple 4-day split: Day 1 - Chest & Triceps, Day 2 - Back & Biceps, Day 3 - Rest, Day 4 - Shoulders, Day 5 - Legs, Day 6 - Cardio/Core, Day 7 - Rest. Want more detail on any day?",
            "For beginners, a 3-day full-body routine works best: Squats, Deadlifts, Bench Press, Rows, Overhead Press. Do this Mon/Wed/Fri with rest days in between. Are you a beginner or intermediate?",
            "A good workout plan depends on your goal. Are you focused on strength, hypertrophy, fat loss, or general fitness? That'll help me tailor the best plan for you.",
            "I'd recommend starting with compound movements 3x per week and adding isolation work as you progress. Consistency matters more than perfection — how many days per week can you commit?"
        ]
    ),
    # Diet / nutrition for fitness
    (
        re.compile(r'\b(diet|nutrition|eat|eating|food|meal|protein|carbs|calories|macros|pre.?workout|post.?workout|supplement)\b', re.IGNORECASE),
        [
            "Nutrition is crucial for fitness results. Focus on lean proteins (chicken, fish, eggs, legumes), complex carbs (oats, rice, sweet potato), and healthy fats (avocado, nuts). What's your main nutritional challenge?",
            "Pre-workout: eat a carb + protein meal 1-2 hours before training (e.g., banana + peanut butter, or rice + chicken). Post-workout: consume protein within 30-60 minutes (e.g., whey shake or eggs). Does that help?",
            "Your protein target should be around 1.6-2.2g per kg of bodyweight if you're trying to build muscle, or at least 1.2g/kg for fat loss to preserve muscle mass. How much do you weigh approximately?",
            "Supplements are secondary to a solid diet, but creatine monohydrate (3-5g/day) is one of the most well-researched and effective for strength and muscle gain. Are you currently taking any supplements?"
        ]
    ),
    # Rest and recovery
    (
        re.compile(r'\b(rest|recovery|sore|soreness|sleep|overtraining|rest day|recover|DOMS|tired|fatigue)\b', re.IGNORECASE),
        [
            "Rest is where muscles actually grow! Aim for 7-9 hours of sleep per night. Skipping rest days is one of the most common mistakes in fitness. How many rest days are you currently taking?",
            "Muscle soreness (DOMS) is normal, especially after new exercises. Light activity like walking or stretching can help. Make sure you're sleeping enough and eating adequate protein for recovery.",
            "Overtraining is real — signs include persistent fatigue, decreased performance, and mood changes. Take at least 1-2 rest days per week and consider a deload week every 4-6 weeks.",
            "Recovery is just as important as training. Prioritize sleep, hydration, and protein intake. Foam rolling and light stretching can also help reduce soreness between sessions."
        ]
    ),
    # Injury / pain
    (
        re.compile(r'\b(injury|injured|pain|hurt|ache|sprain|strain|pulled|knee pain|back pain|shoulder pain|wrist pain)\b', re.IGNORECASE),
        [
            "I'm sorry to hear you're dealing with pain. Please consult a physiotherapist or doctor before continuing to train through an injury — pushing through pain can make things worse.",
            "Injuries need proper attention. Apply the RICE method for acute injuries: Rest, Ice, Compression, Elevation. For anything persistent, please see a medical professional.",
            "Training through injury is risky. Consider switching to low-impact alternatives (swimming, cycling) that don't stress the injured area while you recover. What part of your body is affected?"
        ]
    ),
    # Motivation / consistency
    (
        re.compile(r'\b(motivated|motivation|lazy|give up|can\'t stick|consistency|discipline|habit|procrastinat|demotivat|no energy|skip|skipping)\b', re.IGNORECASE),
        [
            "Motivation gets you started, but discipline keeps you going. Try scheduling your workouts like meetings — non-negotiable appointments with yourself. What time of day works best for you?",
            "Set small, achievable goals each week rather than focusing only on the end goal. Celebrating small wins builds momentum. What's one mini-goal you could hit this week?",
            "It's completely normal to lose motivation sometimes. Try finding a workout partner, joining a class, or switching up your routine to keep things exciting. What part of your routine feels most boring?",
            "Remember why you started! Write down your 'why' and put it somewhere visible. Progress photos, tracking apps, and community support can also keep you accountable. You've got this!"
        ]
    ),
    # Beginner questions
    (
        re.compile(r'\b(beginner|just started|new to (the )?gym|don\'t know where to start|starting out|first time|no experience)\b', re.IGNORECASE),
        [
            "Welcome to your fitness journey! As a beginner, start with 3 full-body workouts per week using compound movements: squats, deadlifts, push-ups, rows, and overhead press. Keep it simple and consistent.",
            "The most important thing as a beginner is learning proper form before adding heavy weight. Consider working with a trainer for a few sessions or watching reputable YouTube tutorials (e.g., AthleanX, Jeff Nippard).",
            "Start slow and build gradually. Beginners typically see great progress in the first 3-6 months — this is called 'newbie gains'. Focus on consistency and progressive overload. What equipment do you have access to?"
        ]
    ),
    # Thank you / positive feedback
    (
        re.compile(r'\b(thank(s| you)|that helps|great advice|awesome|helpful|appreciate)\b', re.IGNORECASE),
        [
            "You're welcome! Remember, the best workout is the one you actually do. Keep showing up!",
            "Glad I could help! Stay consistent and trust the process — results take time but they come!",
            "Anytime! Now go get that workout in. You've got this!"
        ]
    ),
    # Goodbye
    (
        re.compile(r'\b(bye|goodbye|see you|take care|quit|exit)\b', re.IGNORECASE),
        [
            "Goodbye! Stay consistent, stay disciplined, and remember — every rep counts. See you next time!",
            "See you! Keep pushing and don't skip leg day! Take care.",
            "Bye! Remember: the only bad workout is the one that didn't happen. Keep it up!"
        ]
    ),
]

# Default fallback responses
fallback_responses = [
    "That's an interesting question! Could you give me a bit more detail so I can give you the best fitness advice?",
    "I want to make sure I give you the right guidance. Could you clarify what you're working on?",
    "I'm here to help with your fitness journey. Can you tell me more about your goal or concern?",
    "Hmm, I want to make sure I help you correctly. Are you asking about workouts, nutrition, recovery, or motivation?"
]


def reflect(text):
    """Simple pronoun reflection for more natural responses."""
    reflection_map = {
        r'\bI am\b': 'you are',
        r'\bI\'m\b': 'you are',
        r'\bI was\b': 'you were',
        r'\bI\b': 'you',
        r'\bmy\b': 'your',
        r'\bme\b': 'you',
        r'\bmine\b': 'yours',
    }
    for pattern, replacement in reflection_map.items():
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    return text


def get_response(user_input):
    """Match user input against patterns and return an appropriate response."""
    for pattern, responses in patterns:
        match = pattern.search(user_input)
        if match:
            response = random.choice(responses)
            try:
                groups = match.groups()
                if groups:
                    response = response.format(*[g for g in groups if g is not None])
            except (IndexError, KeyError):
                pass
            return response
    return random.choice(fallback_responses)


def chatbot():
    """Run the chatbot in interactive mode."""
    print("=" * 60)
    print(" FitBot — Your Personal Fitness Coaching Chatbot")
    print(" Type 'bye' or 'exit' to end the conversation.")
    print("=" * 60)
    print("FitBot: Hey! I'm FitBot, your personal fitness coach.")
    print("        What fitness goal are you working towards today?\n")

    while True:
        user_input = input("You: ").strip()
        if not user_input:
            continue
        response = get_response(user_input)
        print(f"FitBot: {response}\n")
        if re.search(r'\b(bye|goodbye|exit|quit)\b', user_input, re.IGNORECASE):
            break

# Uncomment to run interactively:
# chatbot()
print("FitBot defined. Run chatbot() to start an interactive session.")
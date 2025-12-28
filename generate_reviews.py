print(">>> SCRIPT STARTED <<<")


"""
Amazon Reviews Dataset Generator - Reviews
This will create: dataset/amazon_reviews.csv

INSTRUCTIONS:
1. Save this file as: generate_reviews.py (anywhere convenient)
2. Run: python generate_reviews.py
3. It will create amazon_reviews.csv in the dataset/ folder
"""

import csv
import random
import os

# Create dataset folder if it doesn't exist
os.makedirs('dataset', exist_ok=True)

# Positive review templates
positive_reviews = [
    "This product is absolutely amazing! Best purchase I've made.",
    "Excellent quality! Highly recommend to everyone.",
    "Love it! Works perfectly and exceeded expectations.",
    "Outstanding product! Worth every single penny.",
    "Perfect! Exactly what I was looking for.",
    "Fantastic quality! Very satisfied with this purchase.",
    "Great product! Fast delivery and excellent packaging.",
    "Superb! Better than I expected. Five stars!",
    "Wonderful purchase! My family loves it.",
    "Brilliant product! Top-notch quality and performance.",
    "Amazing! This product is a game changer for me.",
    "Incredible quality! Can't imagine life without it now.",
    "Best product ever! Absolutely no complaints.",
    "Phenomenal! Exactly as described in listing.",
    "Flawless product! Couldn't be happier with it.",
    "Impressive features and very easy to use!",
    "Perfect purchase! Delivery was super fast too.",
    "Exceptional quality! This is a premium product.",
    "Marvelous! This is exactly what I wanted.",
    "Great value! Much better than similar products.",
    "Awesome quality! Works like a charm every time.",
    "Stunning product! Very well made and durable.",
    "Delighted with purchase! Everything is perfect.",
    "Remarkable quality! Excellent performance so far.",
    "Very happy! This product exceeded all expectations.",
    "Superior quality! Best in its category hands down.",
    "Thrilled! Five stars without any hesitation.",
    "Perfect fit! Works exactly as I hoped it would.",
    "Excellent craftsmanship! Built to last for years.",
    "Love the quality! Definitely buying again.",
]

# Negative review templates
negative_reviews = [
    "Terrible quality. Broke after just one day of use.",
    "Not worth the price at all. Very disappointing.",
    "Worst product I've ever purchased. Complete waste.",
    "Very disappointed. Product doesn't work as advertised.",
    "Horrible experience. Item arrived damaged and broken.",
    "Poor quality materials. Would not recommend to anyone.",
    "Awful product. Had to return it immediately.",
    "Complete garbage. Don't waste your hard-earned money.",
    "Defective product. Stopped working within a week.",
    "Extremely poor quality. Very upset with this purchase.",
    "Useless product. Total rip-off and waste of time.",
    "Low quality. Not satisfied at all with this.",
    "Broke within just a few days. Poor manufacturing.",
    "Disappointing purchase. Not as described in listing.",
    "Faulty product. Customer service was also unhelpful.",
    "Cheaply made. Falls apart very easily unfortunately.",
    "Waste of money. Avoid this product at all costs.",
    "Very poor design. Doesn't work properly at all.",
    "Regret buying this. Complete disappointment overall.",
    "Substandard quality. Not durable whatsoever unfortunately.",
    "Misleading product description. Very frustrated with this.",
    "Arrived broken. Packaging was also very poor quality.",
    "Does not work as promised. Terrible product overall.",
    "Poorly constructed. Broke immediately after opening box.",
    "Horrible quality. Would never buy this brand again.",
    "Complete failure. Stopped working after minimal use.",
    "Very unhappy. Product is absolutely worthless junk.",
    "Terrible experience. Can't recommend this to anyone.",
    "Cheap quality. Definitely not worth buying at all.",
    "Defective from start. Very bad experience overall.",
]

# Neutral review templates
neutral_reviews = [
    "It's okay. Nothing special but it works fine.",
    "Average product. Does the basic job adequately.",
    "Decent quality. Meets basic needs and requirements.",
    "It's fine. Nothing extraordinary about this product.",
    "Acceptable product. Neither particularly good nor bad.",
    "Mediocre. Gets the job done but nothing more.",
    "Standard quality. No major complaints about it.",
    "Okay for the price. Nothing particularly impressive.",
    "Fair product. Could definitely be better though.",
    "It works fine. Not amazing but adequate enough.",
    "Reasonable quality. Meets my basic expectations overall.",
    "Basic product. Does exactly what it claims to.",
    "So-so quality. Nothing really worth writing about.",
    "Middle of the road. Average performance overall.",
    "It's alright. Serves its basic purpose adequately.",
    "Ordinary product. Nothing particularly special here.",
    "Satisfactory. Gets the basic job done well enough.",
    "Plain and simple. Works fine for basic needs.",
    "Not bad, not great. Just okay for the price.",
    "Functional. Nothing more and nothing less really.",
]

def generate_dataset():
    """Generate  reviews with realistic distribution"""
    
    reviews_data = []
    review_id = 1
    
    # Distribution: 50% Positive, 35% Negative, 15% Neutral
    # This mirrors real-world Amazon review patterns
    
    # Generate 1500 Positive reviews
    for i in range(1500):
        review_text = random.choice(positive_reviews)
        rating = random.choice([4, 5, 5, 5])  # Mostly 5 stars
        reviews_data.append([review_id, rating, review_text, "Positive"])
        review_id += 1
    
    # Generate 1050 Negative reviews
    for i in range(1050):
        review_text = random.choice(negative_reviews)
        rating = random.choice([1, 1, 1, 2])  # Mostly 1 star
        reviews_data.append([review_id, rating, review_text, "Negative"])
        review_id += 1
    
    # Generate 450 Neutral reviews
    for i in range(450):
        review_text = random.choice(neutral_reviews)
        rating = 3  # Always 3 stars for neutral
        reviews_data.append([review_id, rating, review_text, "Neutral"])
        review_id += 1
    
    # Shuffle reviews to mix sentiments randomly
    random.shuffle(reviews_data)
    
    # Re-assign sequential IDs after shuffling
    for idx, review in enumerate(reviews_data, 1):
        review[0] = idx
    print("Generated reviews:", len(reviews_data))

    return reviews_data

def save_to_csv(reviews_data):
    """Save reviews to CSV file in dataset folder"""
    
    output_file = 'dataset/amazon_reviews.csv'
    
    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        # Write header
        writer.writerow(['Review_ID', 'Rating', 'Review_Text', 'Sentiment'])
        
        # Write all review data
        writer.writerows(reviews_data)
    
    return output_file

def main():
    """Main function to generate and save dataset"""
    
    print("=" * 70)
    print("🚀 GENERATING AMAZON REVIEWS DATASET")
    print("=" * 70)
    print()
    
    # Generate reviews
    print("📝 Generating  reviews...")
    reviews_data = generate_dataset()
    
    # Save to CSV
    print("💾 Saving to dataset/amazon_reviews.csv...")
    output_file = save_to_csv(reviews_data)
    
    # Calculate statistics
    positive = sum(1 for row in reviews_data if row[3] == 'Positive')
    negative = sum(1 for row in reviews_data if row[3] == 'Negative')
    neutral = sum(1 for row in reviews_data if row[3] == 'Neutral')
    
    # Display results
    print()
    print("=" * 70)
    print("✅ DATASET CREATED SUCCESSFULLY!")
    print("=" * 70)
    print(f"📁 File Location: {output_file}")
    print(f"📊 Total Reviews: {len(reviews_data)}")
    print()
    print("📈 Sentiment Distribution:")
    print(f"   • Positive: {positive:,} reviews ({positive/len(reviews_data)*100:.1f}%)")
    print(f"   • Negative: {negative:,} reviews ({negative/len(reviews_data)*100:.1f}%)")
    print(f"   • Neutral:  {neutral:,} reviews ({neutral/len(reviews_data)*100:.1f}%)")
    print()
    
    # Rating distribution
    ratings = {}
    for review in reviews_data:
        rating = review[1]
        ratings[rating] = ratings.get(rating, 0) + 1
    
    print("⭐ Rating Distribution:")
    for rating in sorted(ratings.keys()):
        print(f"   • {rating} stars: {ratings[rating]:,} reviews")
    
    print()
    print("✅ File 'dataset/amazon_reviews.csv' is ready to use!")
    print("=" * 70)

if __name__ == "__main__":
    main()
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import pickle

# ---------------- TRAINING DATA ----------------

texts = [
    # Refund (25 samples)
    "I want my refund",
    "Please return my money",
    "Refund my order immediately",
    "I need a refund for my purchase",
    "My refund has not been processed",
    "Return my payment",
    "Cancel my order and refund",
    "Money back request",
    "I want a full refund for the damaged item",
    "Please process my refund as soon as possible",
    "I have been waiting for my refund for 2 weeks",
    "I never received my order, please refund",
    "Give me back my money, I returned the product",
    "My refund request was ignored, please help",
    "I want to cancel and get a refund",
    "I am requesting a refund for order #1234",
    "The item was not as described, I want a refund",
    "Refund not received after 10 business days",
    "Please reverse the charge on my account",
    "I would like to dispute this charge and get a refund",
    "When will my refund be issued?",
    "My bank has not received the refund yet",
    "Can you confirm the refund was processed?",
    "I cancelled my subscription, where is my refund?",
    "I am not satisfied and want my money back",

    # Complaint (25 samples)
    "The product is damaged",
    "Very bad quality product",
    "I am unhappy with the service",
    "Worst experience ever",
    "The delivery was very late",
    "Customer service is terrible",
    "I received a broken item",
    "Extremely disappointed with the order",
    "Your service is absolutely horrible",
    "I have been treated very poorly by your staff",
    "The item I received is completely wrong",
    "This is unacceptable, I am filing a complaint",
    "I want to report a problem with my order",
    "Your website is broken and I could not checkout",
    "The packaging was damaged and the product inside was ruined",
    "I have been waiting 3 weeks and still no delivery",
    "Your support team is rude and unhelpful",
    "The product stopped working after one day",
    "I ordered a large but received a small, very disappointing",
    "This is the worst purchase I have ever made",
    "My order arrived completely wrong",
    "The quality is far below what was advertised",
    "I am disgusted with how this was handled",
    "Your delivery partner left my parcel in the rain",
    "I demand an explanation for this terrible service",

    # Inquiry (25 samples)
    "What is the delivery time?",
    "How can I track my order?",
    "Do you have this in size M?",
    "When will my order arrive?",
    "Can you help me with my order?",
    "Is this product available?",
    "How long does shipping take?",
    "Where is my order?",
    "Can I change my delivery address?",
    "Do you ship internationally?",
    "What payment methods do you accept?",
    "Is there a warranty on this product?",
    "How do I return an item?",
    "Can I modify my order after placing it?",
    "What is your return policy?",
    "Do you have a store near me?",
    "How do I contact customer support?",
    "Can I get a discount on bulk orders?",
    "Are there any ongoing promotions or sales?",
    "What are your business hours?",
    "How do I create an account on your website?",
    "Can I pay cash on delivery?",
    "How do I apply a coupon code?",
    "Is the product eco-friendly?",
    "What sizes are available for this item?",

    # Feedback (25 samples)
    "Great service",
    "I love this product",
    "Very satisfied with the experience",
    "Amazing quality",
    "Keep up the good work",
    "Excellent support",
    "Happy with the purchase",
    "Fantastic experience",
    "The delivery was super fast, thank you!",
    "Your team was very helpful and professional",
    "I am impressed with the product quality",
    "Everything went smoothly, great job",
    "I will definitely order again from you",
    "The packaging was beautiful and the product is perfect",
    "I love how easy the checkout process was",
    "Your website is very user-friendly",
    "I recommended your service to all my friends",
    "Outstanding product, exceeded my expectations",
    "The customer service representative was very kind",
    "Superb quality and fast delivery",
    "I am a loyal customer and will keep buying here",
    "Best online shopping experience I have had",
    "The product looks exactly like the pictures, very happy",
    "Thank you for the prompt response to my query",
    "Absolutely love the new collection, keep it up"
]

labels = [
    # Refund
    "refund","refund","refund","refund","refund",
    "refund","refund","refund","refund","refund",
    "refund","refund","refund","refund","refund",
    "refund","refund","refund","refund","refund",
    "refund","refund","refund","refund","refund",

    # Complaint
    "complaint","complaint","complaint","complaint","complaint",
    "complaint","complaint","complaint","complaint","complaint",
    "complaint","complaint","complaint","complaint","complaint",
    "complaint","complaint","complaint","complaint","complaint",
    "complaint","complaint","complaint","complaint","complaint",

    # Inquiry
    "inquiry","inquiry","inquiry","inquiry","inquiry",
    "inquiry","inquiry","inquiry","inquiry","inquiry",
    "inquiry","inquiry","inquiry","inquiry","inquiry",
    "inquiry","inquiry","inquiry","inquiry","inquiry",
    "inquiry","inquiry","inquiry","inquiry","inquiry",

    # Feedback
    "feedback","feedback","feedback","feedback","feedback",
    "feedback","feedback","feedback","feedback","feedback",
    "feedback","feedback","feedback","feedback","feedback",
    "feedback","feedback","feedback","feedback","feedback",
    "feedback","feedback","feedback","feedback","feedback"
]

# ---------------- VECTORIZE ----------------
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(texts)

# ---------------- TRAIN MODEL ----------------
model = MultinomialNB()
model.fit(X, labels)

# ---------------- SAVE FILES ----------------
pickle.dump(model, open("intent_model.pkl", "wb"))
pickle.dump(vectorizer, open("vectorizer.pkl", "wb"))

print("[OK] Model training complete.")
print("Files saved:")
print("  - intent_model.pkl")
print("  - vectorizer.pkl")
print(f"  - Total training samples: {len(texts)}")
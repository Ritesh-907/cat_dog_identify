import streamlit as st
import tensorflow as tf
from tensorflow.keras.models import load_model # type: ignore
from PIL import Image
import numpy as np
import os

# Set page configuration
st.set_page_config(
    page_title="Cat vs Dog Identifier",
    page_icon="🐱🐶",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #FF6B6B;
        text-align: center;
        margin-bottom: 2rem;
    }
    .prediction-box {
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        text-align: center;
    }
    .cat-prediction {
        background-color: #FFEAA7;
        border: 2px solid #FDCB6E;
    }
    .dog-prediction {
        background-color: #74B9FF;
        border: 2px solid #0984E3;
    }
    .upload-box {
        border: 2px dashed #ccc;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_trained_model():
    """Load the trained model with error handling"""
    try:
        model = load_model('cat_dog_identifier.h5')
        return model
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        st.info("Please make sure 'cat_dog_identifier.h5' is in the same directory as this app.")
        return None

def preprocess_image(image):
    """Preprocess the image for model prediction"""
    # Resize image to match model's expected input
    image = image.resize((150, 150))
    
    # Convert to array and normalize
    img_array = np.array(image)
    img_array = img_array / 255.0
    
    # Add batch dimension
    img_array = np.expand_dims(img_array, axis=0)
    
    return img_array

def predict_image(model, image):
    """Make prediction on the image"""
    processed_image = preprocess_image(image)
    prediction = model.predict(processed_image)
    return prediction[0][0]

def main():
    # Header
    st.markdown('<h1 class="main-header">🐱 Cat vs Dog Identifier 🐶</h1>', unsafe_allow_html=True)
    
    # Load model
    model = load_trained_model()
    
    if model is None:
        st.stop()
    
    # Sidebar for information
    with st.sidebar:
        st.header("ℹ️ About")
        st.write("""
        This app uses a trained deep learning model to identify whether an image contains a **cat** or a **dog**.
        
        **How to use:**
        1. Upload an image of a cat or dog
        2. The model will analyze the image
        3. View the prediction results
        
        **Supported formats:** JPG, JPEG, PNG
        """)
        
        st.header("📊 Model Info")
        st.write(f"Input shape: {model.input_shape}")
        st.write(f"Output shape: {model.output_shape}")
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📤 Upload Image")
        
        # File uploader
        uploaded_file = st.file_uploader(
            "Choose an image...",
            type=['jpg', 'jpeg', 'png'],
            help="Upload an image of a cat or dog"
        )
        
        if uploaded_file is not None:
            # Display uploaded image
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_column_width=True)
            
            # Make prediction
            with st.spinner('🔍 Analyzing image...'):
                prediction = predict_image(model, image)
            
            # Display results
            with col2:
                st.subheader("📋 Prediction Results")
                
                # Determine prediction
                if prediction > 0.5:
                    confidence = prediction * 100
                    animal = "Dog"
                    css_class = "dog-prediction"
                    emoji = "🐶"
                else:
                    confidence = (1 - prediction) * 100
                    animal = "Cat"
                    css_class = "cat-prediction"
                    emoji = "🐱"
                
                # Display prediction box
                st.markdown(f"""
                <div class="prediction-box {css_class}">
                    <h2>{emoji} It's a {animal}! {emoji}</h2>
                    <h3>Confidence: {confidence:.2f}%</h3>
                </div>
                """, unsafe_allow_html=True)
                
                # Progress bar for confidence
                st.progress(int(confidence))
                
                # Additional info
                st.info(f"""
                **Prediction Details:**
                - **Animal:** {animal}
                - **Confidence:** {confidence:.2f}%
                - **Raw Score:** {prediction:.4f}
                """)
                
                # Interpretation guide
                with st.expander("📖 How to interpret results"):
                    st.write("""
                    **Interpretation Guide:**
                    - **Score close to 0** → High confidence it's a **Cat** 🐱
                    - **Score close to 1** → High confidence it's a **Dog** 🐶
                    - **Score around 0.5** → Model is uncertain
                    
                    The model outputs a probability between 0 and 1, where:
                    - 0 = Definitely Cat
                    - 1 = Definitely Dog
                    """)
        else:
            with col2:
                st.subheader("📋 Prediction Results")
                st.info("👆 Upload an image to see predictions here!")
                
                # Placeholder image
                st.image("https://via.placeholder.com/300x200/CCCCCC/969696?text=Upload+an+image", 
                        caption="Waiting for image upload...", 
                        use_column_width=True)

    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #666;'>"
        "Built with ❤️ using Streamlit and TensorFlow"
        "</div>", 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
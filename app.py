import streamlit as st
import tensorflow as tf
from tensorflow.keras.models import load_model
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
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_trained_model():
    """Load the trained model with error handling"""
    try:
        model = load_model('cat_dog_identifier.h5')
        st.sidebar.success("✅ Model loaded successfully!")
        st.sidebar.info(f"Model input shape: {model.input_shape}")
        return model
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        st.info("Please make sure 'cat_dog_identifier.h5' is in the same directory as this app.")
        return None

def preprocess_image(image):
    """Preprocess the image for model prediction - FIXED TO 224x224"""
    # Resize image to match model's expected input (224x224)
    image = image.resize((224, 224))
    
    # Convert to array and normalize
    img_array = np.array(image)
    
    # Ensure image has 3 channels (RGB)
    if len(img_array.shape) == 2:  # Grayscale
        img_array = np.stack([img_array] * 3, axis=-1)
    elif img_array.shape[-1] == 4:  # RGBA
        img_array = img_array[:, :, :3]
    
    img_array = img_array / 255.0
    
    # Add batch dimension
    img_array = np.expand_dims(img_array, axis=0)
    
    return img_array

def predict_image(model, image):
    """Make prediction on the image"""
    processed_image = preprocess_image(image)
    prediction = model.predict(processed_image, verbose=0)
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
        st.write(f"**Input shape:** {model.input_shape}")
        st.write(f"**Output shape:** {model.output_shape}")
        st.write("**Required image size:** 224×224 pixels")
    
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
            try:
                # Display uploaded image
                image = Image.open(uploaded_file)
                
                # Convert to RGB if necessary
                if image.mode != 'RGB':
                    image = image.convert('RGB')
                
                st.image(image, caption=f"Uploaded Image ({image.size[0]}x{image.size[1]})", use_container_width=True)
                
                # Show resizing info
                st.info(f"📐 Image will be resized from {image.size} to (224, 224) for model input")
                
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
                    
            except Exception as e:
                st.error(f"Error processing image: {str(e)}")
                st.info("Please try with a different image file.")
                
        else:
            with col2:
                st.subheader("📋 Prediction Results")
                st.info("👆 Upload an image to see predictions here!")
                
                # Display requirements
                st.write("**Model Requirements:**")
                st.write("✅ Image size: 224×224 pixels")
                st.write("✅ Color format: RGB")
                st.write("✅ File types: JPG, JPEG, PNG")

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

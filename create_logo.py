from PIL import Image, ImageDraw, ImageFont
import os

def create_logo():
    # Créer une image de 200x80 pixels
    width, height = 200, 80
    image = Image.new('RGBA', (width, height), (0, 0, 0, 0))  # Fond transparent
    draw = ImageDraw.Draw(image)
    
    # Couleurs
    bg_color = (25, 25, 35)  # Fond sombre
    text_color = (255, 255, 255)  # Texte blanc
    accent_color = (0, 200, 255)  # Bleu accent
    
    # Dessiner le fond
    draw.rectangle([0, 0, width, height], fill=bg_color)
    
    # Dessiner un cercle accent
    draw.ellipse([10, 10, 50, 50], fill=accent_color)
    
    # Ajouter le texte "TTrust"
    try:
        # Essayer d'utiliser une police système
        font = ImageFont.truetype("arial.ttf", 24)
    except:
        # Police par défaut si arial n'est pas disponible
        font = ImageFont.load_default()
    
    # Position du texte
    text_x = 60
    text_y = 25
    
    # Dessiner le texte
    draw.text((text_x, text_y), "TTrust", fill=text_color, font=font)
    
    # Ajouter "Investment" en plus petit
    try:
        small_font = ImageFont.truetype("arial.ttf", 12)
    except:
        small_font = ImageFont.load_default()
    
    draw.text((text_x, text_y + 30), "Investment Platform", fill=(200, 200, 200), font=small_font)
    
    # Sauvegarder l'image
    output_path = os.path.join('static', 'ttrust.png')
    image.save(output_path, 'PNG')
    print(f"✅ Logo créé : {output_path}")

if __name__ == "__main__":
    create_logo()

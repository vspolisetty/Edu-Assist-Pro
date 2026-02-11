# Edu Assist - Smart AI Study Companion

A modern, student-friendly chat interface built with pure HTML, CSS, and JavaScript using Material Design principles.

## Features

- 📚 **Subject & Topic Navigation**: Expandable sidebar with subjects and topics
- 💬 **Interactive Chat**: AI-powered conversations with message actions
- 🎨 **Material Design**: Modern UI with ripple effects and smooth transitions
- 🌓 **Theme Toggle**: Light and dark mode support
- 📊 **XP System**: Gamified learning with progress tracking
- 🔖 **Bookmarks**: Save important messages and resources
- 📱 **Responsive**: Works on desktop, tablet, and mobile devices

## Getting Started

### Option 1: Using Vite (Recommended)

1. Install dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm run dev
```

3. Open your browser to `http://localhost:5173`

### Option 2: Using Python HTTP Server

1. Navigate to the project directory
2. Run the server:
```bash
npm run serve
```

3. Open your browser to `http://localhost:3000`

### Option 3: Using Live Server (VS Code Extension)

1. Install the "Live Server" extension in VS Code
2. Right-click on `index.html`
3. Select "Open with Live Server"

## Project Structure

```
edu-assist-chat-interface/
├── index.html          # Main HTML file
├── style.css           # All styles and Material Design components
├── script.js           # JavaScript functionality
├── sidebar_data.json   # Subject and topic data
├── package.json        # Project configuration
└── README.md          # This file
```

## Customization

### Adding New Subjects
Edit `sidebar_data.json` to add new subjects and topics:

```json
{
  "id": "new_subject",
  "name": "New Subject",
  "icon": "🎯",
  "topics": ["Topic 1", "Topic 2", "Topic 3"]
}
```

### Changing Colors
Modify the CSS variables in `style.css`:

```css
.light-theme {
  --primary-color: #your-color;
  --secondary-color: #your-color;
  --accent-color: #your-color;
}
```

### Adding AI Responses
Extend the `generateAIResponse()` function in `script.js` to add more intelligent responses.

## Browser Support

- Chrome 80+
- Firefox 75+
- Safari 13+
- Edge 80+

## License

MIT License - feel free to use this project for educational purposes.
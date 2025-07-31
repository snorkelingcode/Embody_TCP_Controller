# Embody External Controller

A comprehensive TCP-based control system for the Embody virtual character application, featuring real-time character customization, camera control, and game interaction through both command-line and web interfaces.

## 🎮 Features

### Core Control Systems
- **TCP Communication**: Direct socket connection to Embody application (Port 7777)
- **HTTP Bridge**: Web-friendly HTTP-to-TCP bridge server for browser-based control
- **Web Interface**: Full-featured HTML/CSS/JS controller with real-time sliders
- **Command Line Tools**: Simple Python scripts for quick character manipulation

### Character Customization
- **Presets**: Masculine/Feminine character templates
- **Outfits**: Multiple outfit options (Maid Dress, Pop Star, Kimono, etc.)
- **Hair Styles**: Various hairstyle presets with color customization
- **Morph Targets**: Detailed facial feature adjustments (50+ parameters)
- **Body Scaling**: Bone size modifications for head, chest, limbs, etc.
- **Skin & Eyes**: Skin tone and eye color/saturation controls

### Camera & Scene Control
- **Camera Shots**: Predefined camera angles (Close, Wide, High/Low Angle)
- **Manual Camera**: Precise XYZ position and rotation control
- **Agent Positioning**: Character placement and orientation
- **Level Management**: Scene switching (Lofi, DJ, Medieval, Orbit, etc.)
- **View Modes**: Desktop and mobile optimized views

### Animation & Interaction
- **Facial Expressions**: 20+ emotion presets (Happy, Sad, Angry, etc.)
- **Animations**: Dance and gesture animations
- **Speech Control**: Start/stop speaking animations
- **Weather System**: Random weather generation

## 📁 Project Structure

```
TCP_Test_Script/
├── tcp_test_client.py          # Simple command-line TCP client
├── http_tcp_bridge.py          # HTTP-to-TCP bridge server
├── tcp_controller.html         # Main web interface
├── controller.css              # Web interface styling
├── controller.js               # Web interface JavaScript
├── chargen.py                  # Random character generator
├── value_sender.py             # Game statistics sender
├── CMH.py                      # Character morph handler
├── camera_animator.py          # Camera animation system
├── emote.py                    # Emotion/expression controller
├── entropy.py                  # Randomization utilities
├── play_emotion_from_command.py # Command-based emotion player
├── rand_weather.py             # Weather randomization
├── body_type_glitcher.py       # Body type variation system
├── hair_color_randomizer.py    # Hair color randomization
├── hair_morph_target_randomizer.py # Hair morph controls
├── gym_mode_buffing.py         # Character enhancement system
└── outfit_speed_switch.py      # Quick outfit switching
```

## 🚀 Quick Start

### 1. Start the Embody Application
Ensure your Embody application is running and listening on TCP port 7777.

You can find the download here: https://drive.google.com/file/d/1skgExWRqsK-m3FLZbcuqAYrp8L9xZcAV/view?usp=sharing
Currently only built for Windows. Linux coming soon.

### 2. Launch Bridge Server
```bash
# Start the HTTP-to-TCP bridge
python http_tcp_bridge.py
# Bridge runs on http://127.0.0.1:8080
```

### 3. Web Interface Setup
```bash
# Open TCP controller in your browser
tcp_controller.html
# Connect to bridge and start controlling!
```

## 🌐 Web Interface Features

The web controller (`tcp_controller.html`) provides:

- **Real-time Sliders**: Instant parameter adjustment with live feedback
- **Connection Management**: Easy connect/disconnect with status indicators
- **Organized Sections**: Collapsible categories for different control types
- **Manual Input**: Precise numeric value entry for camera/agent positioning
- **Responsive Design**: Works on desktop and mobile devices

## 🔧 Technical Details

### Network Configuration
- **TCP Port**: 7777 (Embody application)
- **HTTP Bridge Port**: 8080 (Web interface communication)
- **Protocol**: UTF-8 encoded strings with newline termination

### Dependencies
- Python 3.x (no additional packages required)
- Modern web browser with JavaScript support
- Embody application with TCP listener enabled

## 🎯 Use Cases

- **Content Creation**: Streamlined character setup for video/streaming
- **Game Development**: Rapid prototyping of character variations
- **Interactive Experiences**: Real-time character control for performances
- **Animation**: Animate story boards with Metahumans in minutes
- **Education**: Learning character modeling and animation concepts

## 📋 Requirements

- Embody application with TCP listener
- Python 3.x
- Web browser (Chrome, Firefox, Safari, Edge)
- Network access to localhost (127.0.0.1)

## 🤝 Contributing

This is a specialized control system for Embody. Feel free to:
- Add new character presets
- Expand camera control options
- Improve the web interface design
- Add automation scripts
- Enhance error handling

## 📄 License

Open source project for Embody integration and control.

---

**Note**: This project requires the Embody application to be running with TCP listener enabled on port 7777. Ensure your firewall allows local connections on the specified ports.

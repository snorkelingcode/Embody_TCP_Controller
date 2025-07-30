let isConnected = false;
let bridgeUrl = '';

// Initialize the controller when page loads
document.addEventListener('DOMContentLoaded', function() {
    initializeSliders();
    setupEventListeners();
    initializeCameraSliders();
    initializeAgentSliders();
});

// Initialize all sliders with their value displays
function initializeSliders() {
    const sliders = document.querySelectorAll('input[type="range"]');
    sliders.forEach(slider => {
        const valueSpan = document.getElementById(slider.id + 'Value');
        if (valueSpan) {
            updateSliderValue(slider, valueSpan);
            slider.addEventListener('input', () => {
                updateSliderValue(slider, valueSpan);
                sendSliderCommand(slider.id, slider.value);
            });
        }
    });
}

// Update slider value display
function updateSliderValue(slider, valueSpan) {
    const value = parseFloat(slider.value);
    valueSpan.textContent = value.toFixed(2);
}

// Setup event listeners
function setupEventListeners() {
    document.getElementById('connect').addEventListener('click', connect);
    document.getElementById('disconnect').addEventListener('click', disconnect);
    
    // Setup collapsible sections
    const collapsibleSections = document.querySelectorAll('.collapsible h2');
    collapsibleSections.forEach(header => {
        header.addEventListener('click', function() {
            const section = this.parentElement;
            const content = section.querySelector('.collapsible-content');
            section.classList.toggle('collapsed');
            if (section.classList.contains('collapsed')) {
                content.style.maxHeight = '0';
            } else {
                content.style.maxHeight = content.scrollHeight + 'px';
            }
        });
    });
}

// Connect to TCP server via HTTP bridge
async function connect() {
    const host = document.getElementById('host').value;
    const tcpPort = document.getElementById('port').value;
    const httpPort = document.getElementById('httpPort').value;
    
    if (isConnected) {
        updateStatus('Already connected', 'connected');
        return;
    }
    
    // Set bridge URL
    bridgeUrl = `http://${host}:${httpPort}`;
    
    try {
        // Test connection to bridge
        updateStatus('Connecting...', 'disconnected');
        
        const testResponse = await fetch(`${bridgeUrl}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ command: 'TEST' })
        });
        
        if (testResponse.ok) {
            isConnected = true;
            updateStatus(`Connected to TCP ${host}:${tcpPort}`, 'connected');
            console.log(`Connected via HTTP bridge to TCP ${host}:${tcpPort}`);
        } else {
            throw new Error('Bridge server not responding');
        }
        
    } catch (error) {
        isConnected = false;
        updateStatus('Connection Failed - Check Bridge Server', 'disconnected');
        console.error('Connection error:', error);
        alert(`Connection failed!\n\nMake sure the bridge server is running:\npython http_tcp_bridge.py\n\nError: ${error.message}`);
    }
}

// Disconnect from TCP server
function disconnect() {
    isConnected = false;
    bridgeUrl = '';
    updateStatus('Disconnected', 'disconnected');
    console.log('Disconnected from TCP server');
}

// Update connection status display
function updateStatus(message, status) {
    const statusElement = document.getElementById('status');
    statusElement.textContent = message;
    statusElement.className = `status-${status}`;
}

// Send command to TCP server via HTTP bridge
async function sendCommand(command) {
    if (!isConnected || !bridgeUrl) {
        console.warn('Not connected to server');
        updateStatus('Not Connected', 'disconnected');
        return;
    }
    
    try {
        const response = await fetch(bridgeUrl, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ command: command })
        });
        
        const result = await response.json();
        
        if (result.success) {
            console.log('✅ TCP Command sent:', command);
        } else {
            console.error('❌ Failed to send command:', result.error);
            updateStatus('Send Error', 'disconnected');
        }
        
    } catch (error) {
        console.error('❌ Network error:', error);
        updateStatus('Network Error', 'disconnected');
        isConnected = false;
    }
}

// Send slider-based commands
function sendSliderCommand(sliderId, value) {
    const sliderCommands = {
        // Basic controls
        'skinTone': 'SKC.',
        'headSize': 'BNH.',
        'chestSize': 'BNC.',
        'handSize': 'BNHD.',
        'abdomenSize': 'BNA.',
        'armSize': 'BNAR.',
        'legSize': 'BNL.',
        'feetSize': 'BNF.',
        'hairRed': 'HCR.',
        'hairGreen': 'HCG.',
        'hairBlue': 'HCB.',
        'eyeColor': 'EC.',
        'eyeSaturation': 'ES.',
        
        // Morph Targets - Head
        'headTop': 'MTHT.',
        'headSides': 'MTHS.',
        'headBack': 'MTHB.',
        'headBackWidth': 'MTHBW.',
        
        // Morph Targets - Neck
        'neckFrontTop': 'MTNFT.',
        'neckFront': 'MTNF.',
        'neckSides': 'MTNS.',
        'neckBackHigh': 'MTNBH.',
        'neckBackLow': 'MTNBL.',
        'neckDefinition': 'MTND.',
        
        // Morph Targets - Ears
        'earWidth': 'MTEW.',
        'earPoint': 'MTEP.',
        'earlobe': 'MTEL.',
        'earSize': 'MTERS.',
        
        // Morph Targets - Forehead/Temples
        'foreheadCenter': 'MTFHC.',
        'foreheadCurvature': 'MTFHCR.',
        'foreheadSides': 'MTFHS.',
        'temples': 'MTT.',
        
        // Morph Targets - Eyebrows
        'eyebrowHeight': 'MTEBH.',
        'eyebrowWidth': 'MTEBW.',
        'eyebrowArch': 'MTEBA.',
        
        // Morph Targets - Eyes
        'eyeCavity': 'MTEC.',
        'eyeWidth': 'MTEYW.',
        'eyeBags': 'MTEB.',
        'eyeHeight': 'MTEYH.',
        
        // Morph Targets - Nose
        'noseBase': 'MTNB.',
        'noseLength': 'MTNL.',
        'noseWidth': 'MTNW.',
        'nostril': 'MTN.',
        'septum': 'MTS.',
        'noseCrookedness': 'MTNCR.',
        
        // Morph Targets - Cheeks
        'cheekBone': 'MTCB.',
        'cheekTissue': 'MTCT.',
        'cheekDefinition': 'MTCD.',
        
        // Morph Targets - Lips
        'lipsOuter': 'MTLO.',
        'lipsWidth': 'MTLW.',
        'lipsOverlap': 'MTLOV.',
        'lipsCurve': 'MTLCV.',
        'lipsDepth': 'MTLD.',
        'lipsUnderlap': 'MTLU.',
        
        // Morph Targets - Chin/Jaw
        'chinLength': 'MCL.',
        'chinPoint': 'MTCP.',
        'chinWidth': 'MTCW.',
        'jawLower': 'MTJL.',
        'jawHigher': 'MTJH.',
        
        // Morph Targets - Other
        'horns': 'MTH.'
    };
    
    const command = sliderCommands[sliderId];
    if (command) {
        sendCommand(command + value);
    }
}

// Character name command
function sendNameCommand() {
    const name = document.getElementById('characterName').value;
    if (name) {
        sendCommand('NAME.' + name);
    }
}

// Load character command
function sendLoadCommand() {
    const name = document.getElementById('loadName').value;
    if (name) {
        sendCommand('Load.' + name);
    }
}

// Delete character command
function sendDeleteCommand() {
    const name = document.getElementById('deleteName').value;
    if (name) {
        sendCommand('Delete.' + name);
    }
}

// Agent location command
function sendLocation() {
    const x = document.getElementById('locX') ? document.getElementById('locX').value : 0;
    const y = document.getElementById('locY') ? document.getElementById('locY').value : 0;
    const z = document.getElementById('locZ') ? document.getElementById('locZ').value : 0;
    
    const command = `LOC_${x}_${y}_${z}`;
    sendCommand(command);
}

// Agent rotation command
function sendRotation() {
    const x = document.getElementById('rotX') ? document.getElementById('rotX').value : 0;
    const y = document.getElementById('rotY') ? document.getElementById('rotY').value : 0;
    const z = document.getElementById('rotZ') ? document.getElementById('rotZ').value : 0;
    
    const command = `ROT_${x}_${y}_${z}`;
    sendCommand(command);
}

// Initialize camera slider controls
function initializeCameraSliders() {
    // Setup all camera sliders with value updates and command sending
    const cameraSliders = ['positionX', 'positionY', 'positionZ', 'rotationRX', 'rotationRY', 'rotationRZ'];
    
    cameraSliders.forEach(sliderId => {
        const slider = document.getElementById(sliderId);
        const valueSpan = document.getElementById(sliderId + 'Value');
        
        // Update value display
        slider.addEventListener('input', () => {
            const value = parseFloat(slider.value);
            valueSpan.textContent = value.toFixed(3);
            
            // Send camera update immediately when slider changes
            if (document.getElementById('continuousUpdate').checked) {
                sendCameraUpdateFromSliders();
            }
        });
        
        // Initialize display value
        valueSpan.textContent = parseFloat(slider.value).toFixed(3);
    });
    
    // Setup speed and update rate sliders
    setupSliderUpdates('movementSpeed', 'movementSpeedValue');
    setupSliderUpdates('rotationSpeed', 'rotationSpeedValue');
    setupSliderUpdates('updateRate', 'updateRateValue');
}

// Initialize agent slider controls
function initializeAgentSliders() {
    // Setup all agent sliders with value updates and command sending
    const agentSliders = ['agentX', 'agentY', 'agentZ', 'agentRX', 'agentRY', 'agentRZ'];
    
    agentSliders.forEach(sliderId => {
        const slider = document.getElementById(sliderId);
        const valueSpan = document.getElementById(sliderId + 'Value');
        
        if (slider && valueSpan) {
            // Update value display
            slider.addEventListener('input', () => {
                const value = parseFloat(slider.value);
                valueSpan.textContent = value.toFixed(3);
                
                // Send agent update immediately when slider changes
                if (document.getElementById('agentContinuousUpdate') && document.getElementById('agentContinuousUpdate').checked) {
                    sendAgentUpdateFromSliders();
                }
            });
            
            // Initialize display value
            valueSpan.textContent = parseFloat(slider.value).toFixed(3);
        }
    });
    
    // Setup speed sliders
    setupSliderUpdates('agentMovementSpeed', 'agentMovementSpeedValue');
    setupSliderUpdates('agentRotationSpeed', 'agentRotationSpeedValue');
}

// Send camera update from slider values
function sendCameraUpdateFromSliders() {
    const x = parseFloat(document.getElementById('positionX').value).toFixed(3);
    const y = parseFloat(document.getElementById('positionY').value).toFixed(3);
    const z = parseFloat(document.getElementById('positionZ').value).toFixed(3);
    const rx = parseFloat(document.getElementById('rotationRX').value).toFixed(3);
    const ry = parseFloat(document.getElementById('rotationRY').value).toFixed(3);
    const rz = parseFloat(document.getElementById('rotationRZ').value).toFixed(3);
    
    const command = `CAMSTREAM_${x}_${y}_${z}_${rx}_${ry}_${rz}`;
    sendCommand(command);
}

// Send agent update from slider values
function sendAgentUpdateFromSliders() {
    const x = parseFloat(document.getElementById('agentX').value).toFixed(3);
    const y = parseFloat(document.getElementById('agentY').value).toFixed(3);
    const z = parseFloat(document.getElementById('agentZ').value).toFixed(3);
    const rx = parseFloat(document.getElementById('agentRX').value).toFixed(3);
    const ry = parseFloat(document.getElementById('agentRY').value).toFixed(3);
    const rz = parseFloat(document.getElementById('agentRZ').value).toFixed(3);
    
    // Send both location and rotation commands
    const locCommand = `LOC_${x}_${y}_${z}`;
    const rotCommand = `ROT_${rx}_${ry}_${rz}`;
    
    sendCommand(locCommand);
    sendCommand(rotCommand);
}

// Setup slider value updates
function setupSliderUpdates(sliderId, valueId) {
    const slider = document.getElementById(sliderId);
    const valueSpan = document.getElementById(valueId);
    
    slider.addEventListener('input', () => {
        valueSpan.textContent = parseFloat(slider.value).toFixed(1);
    });
}

// Reset camera position
function resetCameraPosition() {
    // Reset all sliders to 0
    const sliders = ['positionX', 'positionY', 'positionZ', 'rotationRX', 'rotationRY', 'rotationRZ'];
    
    sliders.forEach(sliderId => {
        const slider = document.getElementById(sliderId);
        const valueSpan = document.getElementById(sliderId + 'Value');
        
        slider.value = 0;
        valueSpan.textContent = '0.000';
    });
    
    // Send the reset command
    sendCameraUpdateFromSliders();
}

// Reset agent position
function resetAgentPosition() {
    // Reset all sliders to 0
    const sliders = ['agentX', 'agentY', 'agentZ', 'agentRX', 'agentRY', 'agentRZ'];
    
    sliders.forEach(sliderId => {
        const slider = document.getElementById(sliderId);
        const valueSpan = document.getElementById(sliderId + 'Value');
        
        if (slider && valueSpan) {
            slider.value = 0;
            valueSpan.textContent = '0.000';
        }
    });
    
    // Send the reset command
    sendAgentUpdateFromSliders();
}

// Center all sliders (same as reset)
function centerJoysticks() {
    resetCameraPosition();
}

// Center agent sliders (same as reset) 
function centerAgentSliders() {
    resetAgentPosition();
}

// Send manual camera input
function sendManualCamera() {
    const x = parseFloat(document.getElementById('manualX').value) || 0;
    const y = parseFloat(document.getElementById('manualY').value) || 0;
    const z = parseFloat(document.getElementById('manualZ').value) || 0;
    const rx = parseFloat(document.getElementById('manualRX').value) || 0;
    const ry = parseFloat(document.getElementById('manualRY').value) || 0;
    const rz = parseFloat(document.getElementById('manualRZ').value) || 0;
    
    const command = `CAMSTREAM_${x.toFixed(3)}_${y.toFixed(3)}_${z.toFixed(3)}_${rx.toFixed(3)}_${ry.toFixed(3)}_${rz.toFixed(3)}`;
    sendCommand(command);
}

// Send manual agent input
function sendManualAgent() {
    const x = parseFloat(document.getElementById('manualAgentX').value) || 0;
    const y = parseFloat(document.getElementById('manualAgentY').value) || 0;
    const z = parseFloat(document.getElementById('manualAgentZ').value) || 0;
    const rx = parseFloat(document.getElementById('manualAgentRX').value) || 0;
    const ry = parseFloat(document.getElementById('manualAgentRY').value) || 0;
    const rz = parseFloat(document.getElementById('manualAgentRZ').value) || 0;
    
    const locCommand = `LOC_${x.toFixed(3)}_${y.toFixed(3)}_${z.toFixed(3)}`;
    const rotCommand = `ROT_${rx.toFixed(3)}_${ry.toFixed(3)}_${rz.toFixed(3)}`;
    
    sendCommand(locCommand);
    sendCommand(rotCommand);
}

// Send CamLoc command (uses current camera position for agent location)
function sendCamLoc() {
    const x = parseFloat(document.getElementById('positionX').value).toFixed(3);
    const y = parseFloat(document.getElementById('positionY').value).toFixed(3);
    const z = parseFloat(document.getElementById('positionZ').value).toFixed(3);
    
    const command = `CAMLOC_${x}_${y}_${z}`;
    sendCommand(command);
}

// Toggle collapsible sections
function toggleSection(sectionId) {
    const section = document.getElementById(sectionId);
    const toggle = document.getElementById(sectionId + 'Toggle');
    
    if (section.style.display === 'none') {
        section.style.display = 'block';
        toggle.textContent = '▼';
    } else {
        section.style.display = 'none';
        toggle.textContent = '▶';
    }
}

// Keyboard shortcuts
document.addEventListener('keydown', function(event) {
    // Ctrl + Enter to connect/disconnect
    if (event.ctrlKey && event.key === 'Enter') {
        if (isConnected) {
            disconnect();
        } else {
            connect();
        }
        event.preventDefault();
    }
    
    // ESC to quit (sends quit command)
    if (event.key === 'Escape') {
        if (confirm('Send quit command to game?')) {
            sendCommand('QUIT.');
        }
        event.preventDefault();
    }
    
    // R to reset camera
    if (event.key === 'r' || event.key === 'R') {
        resetCameraPosition();
        event.preventDefault();
    }
    
    // C to center joysticks
    if (event.key === 'c' || event.key === 'C') {
        centerJoysticks();
        event.preventDefault();
    }
    
    // A to reset agent position
    if (event.key === 'a' || event.key === 'A') {
        resetAgentPosition();
        event.preventDefault();
    }
    
    // Z to center agent sliders
    if (event.key === 'z' || event.key === 'Z') {
        centerAgentSliders();
        event.preventDefault();
    }
});
const { app, BrowserWindow, ipcMain, Menu, dialog, shell } = require('electron');
const path = require('path');
const Store = require('electron-store');
const fetch = require('node-fetch');

// Initialize persistent storage
const store = new Store();

let mainWindow;
let serverProcess = null;

// Server configuration
const DEFAULT_API_URL = 'http://localhost:8000';
const DEFAULT_STREAMLIT_URL = 'http://localhost:8501';

function createWindow() {
    mainWindow = new BrowserWindow({
        width: 1400,
        height: 900,
        minWidth: 1000,
        minHeight: 700,
        icon: path.join(__dirname, 'build/icon.png'),
        webPreferences: {
            preload: path.join(__dirname, 'preload.js'),
            contextIsolation: true,
            nodeIntegration: false,
            webSecurity: true
        },
        backgroundColor: '#0f172a',
        show: false,
        titleBarStyle: 'default',
        autoHideMenuBar: false
    });

    // Create application menu
    createMenu();

    // Show window when ready
    mainWindow.once('ready-to-show', () => {
        mainWindow.show();
        checkServerConnection();
    });

    // Load the appropriate interface
    const interfaceMode = store.get('interfaceMode', 'chat');
    loadInterface(interfaceMode);

    // Handle external links
    mainWindow.webContents.setWindowOpenHandler(({ url }) => {
        shell.openExternal(url);
        return { action: 'deny' };
    });

    mainWindow.on('closed', () => {
        mainWindow = null;
    });
}

function loadInterface(mode) {
    store.set('interfaceMode', mode);

    if (mode === 'chat') {
        // Load chat-full.html
        const chatPath = path.join(__dirname, '..', 'examples', 'chat-full.html');
        mainWindow.loadFile(chatPath);
    } else if (mode === 'streamlit') {
        // Load Streamlit app
        const streamlitUrl = store.get('streamlitUrl', DEFAULT_STREAMLIT_URL);
        mainWindow.loadURL(streamlitUrl);
    } else if (mode === 'landing') {
        // Load landing page
        const landingPath = path.join(__dirname, '..', 'index.html');
        mainWindow.loadFile(landingPath);
    }
}

async function checkServerConnection() {
    const apiUrl = store.get('apiUrl', DEFAULT_API_URL);

    try {
        const response = await fetch(`${apiUrl}/health`, { timeout: 3000 });
        if (response.ok) {
            console.log('✅ Connected to API server');
            return true;
        }
    } catch (error) {
        console.log('⚠️ Cannot connect to API server');
        showServerNotRunningDialog();
        return false;
    }
}

function showServerNotRunningDialog() {
    dialog.showMessageBox(mainWindow, {
        type: 'warning',
        title: 'Server Not Running',
        message: 'AI Nexus API server is not running',
        detail: 'Please start the server using:\n\npython3 start.py\n\nOr the application may not work correctly.',
        buttons: ['OK', 'Open Documentation'],
        defaultId: 0
    }).then(result => {
        if (result.response === 1) {
            shell.openExternal('https://github.com/your-repo/wiki');
        }
    });
}

function createMenu() {
    const template = [
        {
            label: 'File',
            submenu: [
                {
                    label: 'Reload',
                    accelerator: 'CmdOrCtrl+R',
                    click: () => mainWindow.reload()
                },
                {
                    label: 'Force Reload',
                    accelerator: 'CmdOrCtrl+Shift+R',
                    click: () => mainWindow.webContents.reloadIgnoringCache()
                },
                { type: 'separator' },
                {
                    label: 'Toggle DevTools',
                    accelerator: 'CmdOrCtrl+Shift+I',
                    click: () => mainWindow.webContents.toggleDevTools()
                },
                { type: 'separator' },
                {
                    label: 'Exit',
                    accelerator: 'CmdOrCtrl+Q',
                    click: () => app.quit()
                }
            ]
        },
        {
            label: 'View',
            submenu: [
                {
                    label: 'Web Chat Interface',
                    type: 'radio',
                    checked: store.get('interfaceMode', 'chat') === 'chat',
                    click: () => loadInterface('chat')
                },
                {
                    label: 'Desktop App (Streamlit)',
                    type: 'radio',
                    checked: store.get('interfaceMode', 'chat') === 'streamlit',
                    click: () => loadInterface('streamlit')
                },
                {
                    label: 'Landing Page',
                    type: 'radio',
                    checked: store.get('interfaceMode', 'chat') === 'landing',
                    click: () => loadInterface('landing')
                },
                { type: 'separator' },
                {
                    label: 'Zoom In',
                    accelerator: 'CmdOrCtrl+Plus',
                    click: () => {
                        const level = mainWindow.webContents.getZoomLevel();
                        mainWindow.webContents.setZoomLevel(level + 0.5);
                    }
                },
                {
                    label: 'Zoom Out',
                    accelerator: 'CmdOrCtrl+-',
                    click: () => {
                        const level = mainWindow.webContents.getZoomLevel();
                        mainWindow.webContents.setZoomLevel(level - 0.5);
                    }
                },
                {
                    label: 'Reset Zoom',
                    accelerator: 'CmdOrCtrl+0',
                    click: () => mainWindow.webContents.setZoomLevel(0)
                }
            ]
        },
        {
            label: 'Settings',
            submenu: [
                {
                    label: 'Server Configuration',
                    click: () => showServerConfigDialog()
                },
                {
                    label: 'Check Server Status',
                    click: () => checkServerConnection()
                },
                { type: 'separator' },
                {
                    label: 'Clear Cache',
                    click: () => {
                        mainWindow.webContents.session.clearCache();
                        dialog.showMessageBox(mainWindow, {
                            type: 'info',
                            message: 'Cache cleared successfully'
                        });
                    }
                }
            ]
        },
        {
            label: 'Help',
            submenu: [
                {
                    label: 'Documentation',
                    click: () => shell.openExternal('https://github.com/your-repo/wiki')
                },
                {
                    label: 'Report Issue',
                    click: () => shell.openExternal('https://github.com/your-repo/issues')
                },
                { type: 'separator' },
                {
                    label: 'About AI Nexus',
                    click: () => {
                        dialog.showMessageBox(mainWindow, {
                            type: 'info',
                            title: 'About AI Nexus',
                            message: 'AI Nexus Desktop',
                            detail: `Version: ${app.getVersion()}\nElectron: ${process.versions.electron}\nChrome: ${process.versions.chrome}\nNode.js: ${process.versions.node}`
                        });
                    }
                }
            ]
        }
    ];

    const menu = Menu.buildFromTemplate(template);
    Menu.setApplicationMenu(menu);
}

function showServerConfigDialog() {
    // This would show a dialog to configure server URLs
    // For now, using simple input dialogs
    dialog.showMessageBox(mainWindow, {
        type: 'info',
        title: 'Server Configuration',
        message: 'Configure server URLs in your .env file',
        detail: `Current API URL: ${store.get('apiUrl', DEFAULT_API_URL)}\nCurrent Streamlit URL: ${store.get('streamlitUrl', DEFAULT_STREAMLIT_URL)}\n\nEdit .env file to change these settings.`,
        buttons: ['OK']
    });
}

// App lifecycle
app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

app.on('activate', () => {
    if (mainWindow === null) {
        createWindow();
    }
});

// IPC handlers
ipcMain.handle('get-setting', (event, key) => {
    return store.get(key);
});

ipcMain.handle('set-setting', (event, key, value) => {
    store.set(key, value);
    return true;
});

ipcMain.handle('check-server', async () => {
    return await checkServerConnection();
});

// Handle deep links (optional for future use)
app.setAsDefaultProtocolClient('ainexus');

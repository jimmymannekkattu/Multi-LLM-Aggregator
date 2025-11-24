const { contextBridge, ipcRenderer } = require('electron');

// Expose protected methods that allow the renderer process to use
// ipcRenderer without exposing the entire object
contextBridge.exposeInMainWorld('electronAPI', {
    getSetting: (key) => ipcRenderer.invoke('get-setting', key),
    setSetting: (key, value) => ipcRenderer.invoke('set-setting', key, value),
    checkServer: () => ipcRenderer.invoke('check-server'),
    platform: process.platform,
    versions: {
        node: process.versions.node,
        chrome: process.versions.chrome,
        electron: process.versions.electron
    }
});

// Add app information
contextBridge.exposeInMainWorld('appInfo', {
    name: 'AI Nexus Desktop',
    version: require('./package.json').version,
    isElectron: true
});

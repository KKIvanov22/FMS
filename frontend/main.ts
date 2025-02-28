import { app, BrowserWindow, Menu,ipcMain } from 'electron';
import * as path from 'path';

function createWindow() {
  const win = new BrowserWindow({
    width: 1280,
    height: 800,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      nodeIntegration: true,
      contextIsolation: false,
      webviewTag: true, // Enable <webview> tag
      sandbox: false // Disable sandbox to allow pop-ups
    },
    autoHideMenuBar: true
  });

  win.loadFile(path.join(__dirname, '../index.html'));

  Menu.setApplicationMenu(null);
}

app.whenReady().then(() => {
  createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});
ipcMain.on("reload-window", (event) => {
  let win = BrowserWindow.getFocusedWindow();
  if (win) win.reload();
});
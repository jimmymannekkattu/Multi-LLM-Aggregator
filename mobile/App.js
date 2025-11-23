import React, { useState, useEffect } from 'react';
import { StyleSheet, Text, View, TextInput, TouchableOpacity, ScrollView, SafeAreaView, Modal, FlatList, ActivityIndicator } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';

// --- CONFIG ---
const DEFAULT_SERVER = "http://192.168.1.X:8000";

export default function App() {
    const [serverUrl, setServerUrl] = useState(DEFAULT_SERVER);
    const [activeTab, setActiveTab] = useState('chat'); // chat, history, settings

    // Chat State
    const [query, setQuery] = useState('');
    const [messages, setMessages] = useState([]);
    const [loading, setLoading] = useState(false);

    // History State
    const [history, setHistory] = useState([]);
    const [loadingHistory, setLoadingHistory] = useState(false);

    // Settings State
    const [availableModels, setAvailableModels] = useState({ online: [], offline: [] });
    const [selectedOnline, setSelectedOnline] = useState([]);
    const [selectedOffline, setSelectedOffline] = useState([]);

    useEffect(() => {
        loadSettings();
    }, []);

    const loadSettings = async () => {
        try {
            const savedUrl = await AsyncStorage.getItem('serverUrl');
            if (savedUrl) setServerUrl(savedUrl);
            fetchModels(savedUrl || DEFAULT_SERVER);
        } catch (e) { }
    };

    const fetchModels = async (url) => {
        try {
            const res = await fetch(`${url}/models`);
            const data = await res.json();
            setAvailableModels(data);
        } catch (e) {
            console.log("Failed to fetch models");
        }
    };

    const fetchHistory = async () => {
        setLoadingHistory(true);
        try {
            const res = await fetch(`${serverUrl}/history`);
            const data = await res.json();
            if (data.history) setHistory(data.history);
        } catch (e) {
            alert("Failed to fetch history");
        }
        setLoadingHistory(false);
    };

    const sendMessage = async () => {
        if (!query.trim()) return;

        const userMsg = { role: 'user', content: query };
        setMessages(prev => [...prev, userMsg]);
        setQuery('');
        setLoading(true);

        try {
            const res = await fetch(`${serverUrl}/chat`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    query: userMsg.content,
                    online_models: selectedOnline,
                    offline_models: selectedOffline,
                    use_memory: true
                })
            });

            const data = await res.json();
            const aiMsg = { role: 'ai', content: data.final_answer };
            setMessages(prev => [...prev, aiMsg]);
        } catch (e) {
            setMessages(prev => [...prev, { role: 'error', content: "Error connecting to server." }]);
        }
        setLoading(false);
    };

    // --- RENDERERS ---

    const renderChat = () => (
        <View style={styles.tabContent}>
            <ScrollView style={styles.chatContainer}>
                {messages.map((msg, i) => (
                    <View key={i} style={[styles.bubble, msg.role === 'user' ? styles.userBubble : styles.aiBubble]}>
                        <Text style={styles.bubbleText}>{msg.content}</Text>
                    </View>
                ))}
                {loading && <ActivityIndicator size="small" color="#ff4b4b" />}
            </ScrollView>
            <View style={styles.inputArea}>
                <TextInput
                    style={styles.input}
                    value={query}
                    onChangeText={setQuery}
                    placeholder="Ask the Swarm..."
                    placeholderTextColor="#666"
                />
                <TouchableOpacity style={styles.sendBtn} onPress={sendMessage}>
                    <Text style={styles.btnText}>🚀</Text>
                </TouchableOpacity>
            </View>
        </View>
    );

    const renderHistory = () => (
        <View style={styles.tabContent}>
            <TouchableOpacity style={styles.refreshBtn} onPress={fetchHistory}>
                <Text style={styles.btnText}>🔄 Refresh History</Text>
            </TouchableOpacity>
            {loadingHistory ? <ActivityIndicator color="#ff4b4b" /> : (
                <FlatList
                    data={history}
                    keyExtractor={(item) => item.id}
                    renderItem={({ item }) => (
                        <View style={styles.historyCard}>
                            <Text style={styles.historyQ}>Q: {item.query}</Text>
                            <Text style={styles.historyA} numberOfLines={3}>A: {item.answer}</Text>
                            <Text style={styles.historyMeta}>{item.timestamp}</Text>
                        </View>
                    )}
                />
            )}
        </View>
    );

    const renderSettings = () => (
        <ScrollView style={styles.tabContent}>
            <Text style={styles.label}>Server URL</Text>
            <TextInput
                style={styles.input}
                value={serverUrl}
                onChangeText={(t) => { setServerUrl(t); AsyncStorage.setItem('serverUrl', t); }}
            />

            <Text style={styles.label}>Online Models</Text>
            {availableModels.online.map(m => (
                <TouchableOpacity
                    key={m}
                    style={[styles.checkbox, selectedOnline.includes(m) && styles.checked]}
                    onPress={() => {
                        if (selectedOnline.includes(m)) setSelectedOnline(prev => prev.filter(x => x !== m));
                        else setSelectedOnline(prev => [...prev, m]);
                    }}
                >
                    <Text style={styles.checkboxText}>{m}</Text>
                </TouchableOpacity>
            ))}

            <Text style={styles.label}>Offline Models</Text>
            {availableModels.offline.map(m => (
                <TouchableOpacity
                    key={m}
                    style={[styles.checkbox, selectedOffline.includes(m) && styles.checked]}
                    onPress={() => {
                        if (selectedOffline.includes(m)) setSelectedOffline(prev => prev.filter(x => x !== m));
                        else setSelectedOffline(prev => [...prev, m]);
                    }}
                >
                    <Text style={styles.checkboxText}>{m}</Text>
                </TouchableOpacity>
            ))}
        </ScrollView>
    );

    return (
        <SafeAreaView style={styles.container}>
            <View style={styles.header}>
                <Text style={styles.title}>🤖 AI Nexus Mobile</Text>
            </View>

            {activeTab === 'chat' && renderChat()}
            {activeTab === 'history' && renderHistory()}
            {activeTab === 'settings' && renderSettings()}

            <View style={styles.navBar}>
                <TouchableOpacity style={styles.navBtn} onPress={() => setActiveTab('chat')}>
                    <Text style={[styles.navText, activeTab === 'chat' && styles.activeNav]}>💬 Chat</Text>
                </TouchableOpacity>
                <TouchableOpacity style={styles.navBtn} onPress={() => { setActiveTab('history'); fetchHistory(); }}>
                    <Text style={[styles.navText, activeTab === 'history' && styles.activeNav]}>📜 History</Text>
                </TouchableOpacity>
                <TouchableOpacity style={styles.navBtn} onPress={() => setActiveTab('settings')}>
                    <Text style={[styles.navText, activeTab === 'settings' && styles.activeNav]}>⚙️ Settings</Text>
                </TouchableOpacity>
            </View>
        </SafeAreaView>
    );
}

const styles = StyleSheet.create({
    container: { flex: 1, backgroundColor: '#0e1117' },
    header: { padding: 20, borderBottomWidth: 1, borderBottomColor: '#333', alignItems: 'center' },
    title: { color: '#fff', fontSize: 20, fontWeight: 'bold' },
    tabContent: { flex: 1, padding: 15 },
    navBar: { flexDirection: 'row', borderTopWidth: 1, borderTopColor: '#333', padding: 15 },
    navBtn: { flex: 1, alignItems: 'center' },
    navText: { color: '#666', fontSize: 16 },
    activeNav: { color: '#ff4b4b', fontWeight: 'bold' },

    // Chat
    chatContainer: { flex: 1 },
    bubble: { padding: 15, borderRadius: 15, marginBottom: 10, maxWidth: '80%' },
    userBubble: { backgroundColor: '#ff4b4b', alignSelf: 'flex-end' },
    aiBubble: { backgroundColor: '#262730', alignSelf: 'flex-start' },
    bubbleText: { color: '#fff' },
    inputArea: { flexDirection: 'row', marginTop: 10 },
    input: { flex: 1, backgroundColor: '#262730', color: '#fff', padding: 15, borderRadius: 25, marginRight: 10 },
    sendBtn: { backgroundColor: '#ff4b4b', padding: 15, borderRadius: 25, justifyContent: 'center' },
    btnText: { color: '#fff', fontWeight: 'bold', textAlign: 'center' },

    // History
    refreshBtn: { backgroundColor: '#262730', padding: 10, borderRadius: 10, marginBottom: 15 },
    historyCard: { backgroundColor: '#1e1e1e', padding: 15, borderRadius: 10, marginBottom: 10, borderLeftWidth: 3, borderLeftColor: '#ff4b4b' },
    historyQ: { color: '#fff', fontWeight: 'bold', marginBottom: 5 },
    historyA: { color: '#ccc', marginBottom: 5 },
    historyMeta: { color: '#666', fontSize: 12 },

    // Settings
    label: { color: '#ff4b4b', marginTop: 20, marginBottom: 10, fontWeight: 'bold' },
    checkbox: { backgroundColor: '#262730', padding: 15, borderRadius: 10, marginBottom: 5 },
    checked: { backgroundColor: '#ff4b4b' },
    checkboxText: { color: '#fff' }
});

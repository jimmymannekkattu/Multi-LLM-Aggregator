import React, { useState, useEffect } from 'react';
import {
    SafeAreaView,
    ScrollView,
    StatusBar,
    StyleSheet,
    Text,
    TextInput,
    TouchableOpacity,
    View,
    ActivityIndicator,
    Alert,
} from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import axios from 'axios';
import Markdown from 'react-native-markdown-display';

const App = () => {
    const [apiUrl, setApiUrl] = useState('http://localhost:8000');
    const [messages, setMessages] = useState([]);
    const [inputText, setInputText] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [selectedModels, setSelectedModels] = useState(['Free Web (g4f)']);
    const [availableModels, setAvailableModels] = useState({ online: [], offline: [] });
    const [isConnected, setIsConnected] = useState(false);

    useEffect(() => {
        loadSettings();
        checkConnection();
    }, []);

    const loadSettings = async () => {
        try {
            const savedUrl = await AsyncStorage.getItem('apiUrl');
            const savedModels = await AsyncStorage.getItem('selectedModels');

            if (savedUrl) setApiUrl(savedUrl);
            if (savedModels) setSelectedModels(JSON.parse(savedModels));
        } catch (error) {
            console.error('Error loading settings:', error);
        }
    };

    const saveSettings = async () => {
        try {
            await AsyncStorage.setItem('apiUrl', apiUrl);
            await AsyncStorage.setItem('selectedModels', JSON.stringify(selectedModels));
        } catch (error) {
            console.error('Error saving settings:', error);
        }
    };

    const checkConnection = async () => {
        try {
            const response = await axios.get(`${apiUrl}/health`, { timeout: 3000 });
            setIsConnected(response.data.status === 'online');
            if (response.data.status === 'online') {
                fetchModels();
            }
        } catch (error) {
            setIsConnected(false);
            console.error('Connection error:', error);
        }
    };

    const fetchModels = async () => {
        try {
            const response = await axios.get(`${apiUrl}/models`);
            setAvailableModels(response.data);
        } catch (error) {
            console.error('Error fetching models:', error);
        }
    };

    const sendMessage = async () => {
        if (!inputText.trim() || !isConnected) return;

        const userMessage = { role: 'user', content: inputText };
        setMessages(prev => [...prev, userMessage]);
        setInputText('');
        setIsLoading(true);

        try {
            const response = await axios.post(`${apiUrl}/chat`, {
                query: inputText,
                online_models: selectedModels,
                offline_models: [],
                use_memory: true
            });

            const aiMessage = {
                role: 'assistant',
                content: response.data.final_answer
            };
            setMessages(prev => [...prev, aiMessage]);
        } catch (error) {
            Alert.alert('Error', 'Failed to get response from server');
            console.error('Send message error:', error);
        } finally {
            setIsLoading(false);
        }
    };

    const renderMessage = (message, index) => (
        <View
            key={index}
            style={[
                styles.messageBubble,
                message.role === 'user' ? styles.userMessage : styles.aiMessage
            ]}
        >
            {message.role === 'assistant' ? (
                <Markdown style={markdownStyles}>{message.content}</Markdown>
            ) : (
                <Text style={styles.messageText}>{message.content}</Text>
            )}
        </View>
    );

    return (
        <SafeAreaView style={styles.container}>
            <StatusBar barStyle="light-content" backgroundColor="#1e293b" />

            {/* Header */}
            <View style={styles.header}>
                <Text style={styles.headerTitle}>🤖 AI Nexus</Text>
                <View style={styles.statusIndicator}>
                    <View style={[styles.statusDot, isConnected ? styles.connected : styles.disconnected]} />
                    <Text style={styles.statusText}>
                        {isConnected ? 'Connected' : 'Disconnected'}
                    </Text>
                </View>
            </View>

            {/* Messages */}
            <ScrollView
                style={styles.messagesContainer}
                contentContainerStyle={styles.messagesContent}
            >
                {messages.length === 0 && (
                    <View style={styles.emptyState}>
                        <Text style={styles.emptyStateText}>👋 Welcome to AI Nexus!</Text>
                        <Text style={styles.emptyStateSubtext}>
                            Start a conversation by typing a message below
                        </Text>
                    </View>
                )}
                {messages.map(renderMessage)}
                {isLoading && (
                    <View style={styles.loadingContainer}>
                        <ActivityIndicator size="large" color="#667eea" />
                        <Text style={styles.loadingText}>Thinking...</Text>
                    </View>
                )}
            </ScrollView>

            {/* Input Area */}
            <View style={styles.inputContainer}>
                <TextInput
                    style={styles.input}
                    placeholder="Ask me anything..."
                    placeholderTextColor="#94a3b8"
                    value={inputText}
                    onChangeText={setInputText}
                    onSubmitEditing={sendMessage}
                    editable={isConnected && !isLoading}
                    multiline
                />
                <TouchableOpacity
                    style={[styles.sendButton, (!isConnected || isLoading) && styles.sendButtonDisabled]}
                    onPress={sendMessage}
                    disabled={!isConnected || isLoading}
                >
                    <Text style={styles.sendButtonText}>Send</Text>
                </TouchableOpacity>
            </View>
        </SafeAreaView>
    );
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#0f172a',
    },
    header: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center',
        padding: 16,
        backgroundColor: '#1e293b',
        borderBottomWidth: 1,
        borderBottomColor: '#334155',
    },
    headerTitle: {
        fontSize: 20,
        fontWeight: '700',
        color: '#f8fafc',
    },
    statusIndicator: {
        flexDirection: 'row',
        alignItems: 'center',
        gap: 6,
    },
    statusDot: {
        width: 8,
        height: 8,
        borderRadius: 4,
    },
    connected: {
        backgroundColor: '#10b981',
    },
    disconnected: {
        backgroundColor: '#ef4444',
    },
    statusText: {
        fontSize: 12,
        color: '#cbd5e1',
    },
    messagesContainer: {
        flex: 1,
    },
    messagesContent: {
        padding: 16,
    },
    emptyState: {
        alignItems: 'center',
        justifyContent: 'center',
        paddingVertical: 60,
    },
    emptyStateText: {
        fontSize: 24,
        fontWeight: '600',
        color: '#f8fafc',
        marginBottom: 8,
    },
    emptyStateSubtext: {
        fontSize: 14,
        color: '#94a3b8',
        textAlign: 'center',
    },
    messageBubble: {
        maxWidth: '85%',
        padding: 12,
        borderRadius: 16,
        marginBottom: 12,
    },
    userMessage: {
        alignSelf: 'flex-end',
        backgroundColor: '#667eea',
        borderBottomRightRadius: 4,
    },
    aiMessage: {
        alignSelf: 'flex-start',
        backgroundColor: '#1e293b',
        borderBottomLeftRadius: 4,
        borderWidth: 1,
        borderColor: '#334155',
    },
    messageText: {
        fontSize: 15,
        color: '#f8fafc',
        lineHeight: 22,
    },
    loadingContainer: {
        alignItems: 'center',
        padding: 20,
    },
    loadingText: {
        marginTop: 8,
        color: '#cbd5e1',
        fontSize: 14,
    },
    inputContainer: {
        flexDirection: 'row',
        padding: 16,
        backgroundColor: '#1e293b',
        borderTopWidth: 1,
        borderTopColor: '#334155',
        gap: 12,
    },
    input: {
        flex: 1,
        backgroundColor: '#334155',
        borderRadius: 24,
        paddingHorizontal: 16,
        paddingVertical: 12,
        color: '#f8fafc',
        fontSize: 15,
        maxHeight: 100,
    },
    sendButton: {
        backgroundColor: '#667eea',
        borderRadius: 24,
        paddingHorizontal: 20,
        paddingVertical: 12,
        justifyContent: 'center',
    },
    sendButtonDisabled: {
        backgroundColor: '#475569',
        opacity: 0.5,
    },
    sendButtonText: {
        color: '#ffffff',
        fontSize: 15,
        fontWeight: '600',
    },
});

const markdownStyles = {
    body: {
        color: '#f8fafc',
        fontSize: 15,
    },
    code_inline: {
        backgroundColor: '#334155',
        color: '#60a5fa',
        paddingHorizontal: 4,
        borderRadius: 3,
    },
    code_block: {
        backgroundColor: '#334155',
        padding: 12,
        borderRadius: 8,
    },
};

export default App;

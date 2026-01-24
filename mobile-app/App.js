import React, { useState, useEffect, useRef } from 'react';
import {
  StyleSheet, Text, View, ScrollView, TouchableOpacity, TextInput,
  Switch, StatusBar, Image, Platform, FlatList, SafeAreaView
} from 'react-native';
import { NavigationContainer, DefaultTheme as NavTheme } from '@react-navigation/native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { SafeAreaProvider } from 'react-native-safe-area-context';
import { LinearGradient } from 'expo-linear-gradient';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { MaterialCommunityIcons, Ionicons, FontAwesome5 } from '@expo/vector-icons';
import * as Speech from 'expo-speech';

// --- THEME ---
const THEME = {
  bg: '#0B0B0B',
  surface: '#151515',
  card: '#1E1E1E',
  primary: '#E6D48F', // Soft Gold
  secondary: '#BEE8D0', // Mint
  textPrimary: '#FFFFFF',
  textSecondary: '#9CA3AF',
  border: 'rgba(255,255,255,0.05)',
  danger: '#EF4444',
  success: '#10B981',
};

// --- SCREENS ---

function ConnectionOverlay({ isConnected, onConnect, ip, setIp, onDemo }) {
  if (isConnected) return null;

  return (
    <View style={[styles.overlay, { zIndex: 999 }]}>
      <StatusBar barStyle="light-content" backgroundColor="#000" />
      <View style={{ alignItems: 'center', padding: 20 }}>
        <MaterialCommunityIcons name="broadcast" size={64} color={THEME.primary} style={{ marginBottom: 20 }} />
        <Text style={styles.h1}>SignSpeak</Text>
        <Text style={styles.subtitle}>Mobile Companion</Text>

        <TextInput
          style={styles.input}
          placeholder="PC IP Address (e.g. 192.168.1.5)"
          placeholderTextColor="#666"
          value={ip}
          onChangeText={setIp}
          keyboardType="numeric"
        />

        <TouchableOpacity style={styles.btnPrimary} onPress={onConnect}>
          <Text style={styles.btnText}>Connect Scanner</Text>
        </TouchableOpacity>

        <TouchableOpacity style={{ marginTop: 20 }} onPress={onDemo}>
          <Text style={{ color: '#666' }}>Enter Demo Mode</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
}

function DashboardScreen({ gesture, sentence, latency, autoSpeak, speak }) {
  return (
    <SafeAreaView style={styles.container}>
      <ScrollView contentContainerStyle={styles.content}>

        {/* HEADER */}
        <View style={styles.header}>
          <Text style={styles.headerTitle}>Dashboard</Text>
          <View style={styles.avatar}>
            <Text style={{ color: THEME.primary, fontWeight: 'bold' }}>S</Text>
          </View>
        </View>

        {/* HERO CARD */}
        <LinearGradient
          colors={['#1E1E1E', '#151515']}
          style={styles.heroCard}
        >
          <View style={styles.rowBetween}>
            <Text style={styles.cardTitle}>Live Gesture Recognition</Text>
            <MaterialCommunityIcons name="broadcast" color={THEME.primary} size={20} />
          </View>

          <Text style={styles.heroText}>
            {gesture === 'WAITING' ? '...' : gesture}
          </Text>

          <View style={styles.badge}>
            <Text style={styles.badgeText}>
              Confidence: {gesture === 'WAITING' ? '0%' : '94%'}
            </Text>
          </View>

          <View style={{ flexDirection: 'row', alignItems: 'center', marginTop: 15 }}>
            <Ionicons name="ellipse" size={8} color="#10B981" style={{ marginRight: 6 }} />
            <Text style={{ color: THEME.textSecondary, fontSize: 12 }}>Gesture Stable</Text>
          </View>
        </LinearGradient>

        {/* AI SENTENCE */}
        <View style={[styles.card, { borderLeftWidth: 3, borderLeftColor: THEME.secondary, marginTop: 16 }]}>
          <View style={styles.rowBetween}>
            <Text style={styles.cardTitle}>AI Sentence</Text>
            <MaterialCommunityIcons name="brain" color={THEME.secondary} size={20} />
          </View>

          <Text style={styles.sentenceText}>"{sentence}"</Text>

          <View style={styles.rowStart}>
            <MaterialCommunityIcons name="sparkles" size={14} color={THEME.secondary} style={{ marginRight: 6 }} />
            <Text style={{ color: THEME.secondary, fontSize: 12 }}>Powered by Gemini</Text>
          </View>
        </View>

        {/* STATS */}
        <View style={styles.statusRow}>
          <View style={styles.statCard}>
            <Text style={styles.statLabel}>Audio</Text>
            <Text style={[styles.statValue, { color: THEME.primary }]}>{autoSpeak ? 'ON' : 'OFF'}</Text>
          </View>
          <View style={styles.statCard}>
            <Text style={styles.statLabel}>Lang</Text>
            <Text style={styles.statValue}>EN</Text>
          </View>
          <View style={styles.statCard}>
            <Text style={styles.statLabel}>Latency</Text>
            <Text style={[styles.statValue, { color: THEME.primary }]}>{latency}ms</Text>
          </View>
        </View>

        {/* FAB */}
        <TouchableOpacity style={styles.btnPrimary} onPress={() => speak(sentence)}>
          <Ionicons name="volume-high" size={20} color="black" style={{ marginRight: 10 }} />
          <Text style={styles.btnText}>Speak Now</Text>
        </TouchableOpacity>

      </ScrollView>
    </SafeAreaView>
  );
}

function AnalyticsScreen() {
  const data = [40, 70, 50, 90, 60, 80, 95];

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.headerTitle}>Analytics</Text>
      </View>
      <ScrollView contentContainerStyle={styles.content}>

        {/* CHART */}
        <View style={styles.card}>
          <Text style={styles.cardTitle}>Gesture Accuracy</Text>
          <View style={styles.chartContainer}>
            {data.map((h, i) => (
              <View key={i} style={styles.barContainer}>
                <View style={[styles.bar, { height: h + '%', opacity: i === 6 ? 1 : 0.4 }]} />
              </View>
            ))}
          </View>
          <Text style={styles.chartLegend}>Last 7 Sessions</Text>
        </View>

        {/* SUMMARY */}
        <View style={[styles.card, { marginTop: 16 }]}>
          <Text style={styles.cardTitle}>Session Summary</Text>
          <View style={styles.settingRow}>
            <Text style={{ color: THEME.textSecondary }}>Total Gestures</Text>
            <Text style={styles.statValue}>1,240</Text>
          </View>
          <View style={styles.settingRow}>
            <Text style={{ color: THEME.textSecondary }}>Sentences</Text>
            <Text style={styles.statValue}>85</Text>
          </View>
          <View style={styles.settingRow}>
            <Text style={{ color: THEME.textSecondary }}>Avg Accuracy</Text>
            <Text style={[styles.statValue, { color: THEME.primary }]}>92%</Text>
          </View>
        </View>

      </ScrollView>
    </SafeAreaView>
  );
}

function HistoryScreen({ logs }) {
  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.headerTitle}>History</Text>
      </View>
      <FlatList
        data={logs}
        keyExtractor={item => item.id.toString()}
        contentContainerStyle={styles.content}
        ListEmptyComponent={
          <Text style={{ color: '#666', textAlign: 'center', marginTop: 40 }}>No recent activity</Text>
        }
        renderItem={({ item }) => (
          <View style={styles.logItem}>
            <View>
              <Text style={{ color: 'white', fontWeight: '500' }}>{item.message}</Text>
              <Text style={{ color: '#666', fontSize: 12 }}>{item.time}</Text>
            </View>
            <Ionicons name="checkmark-circle" color={THEME.success} size={20} />
          </View>
        )}
      />
    </SafeAreaView>
  );
}

function SettingsScreen({ ip, setIp, autoSpeak, setAutoSpeak, language, setLanguage }) {
  const languages = [
    { code: 'en', name: 'English (US)' },
    { code: 'hi', name: 'Hindi' },
    { code: 'mr', name: 'Marathi' },
    { code: 'es', name: 'Spanish' },
    { code: 'fr', name: 'French' },
    { code: 'de', name: 'German' },
    { code: 'zh', name: 'Chinese' },
    { code: 'ja', name: 'Japanese' },
    { code: 'ar', name: 'Arabic' },
  ];

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.headerTitle}>Preferences</Text>
      </View>
      <ScrollView contentContainerStyle={styles.content}>

        {/* CONNECTION */}
        <View style={styles.card}>
          <Text style={styles.cardTitle}>Connection</Text>
          <Text style={styles.label}>PC IP Address</Text>
          <TextInput
            style={[styles.input, { marginBottom: 0 }]}
            value={ip}
            onChangeText={setIp}
            placeholder="192.168.X.X"
            placeholderTextColor="#666"
          />
        </View>

        {/* TOGGLES */}
        <View style={[styles.card, { marginTop: 16 }]}>
          <Text style={styles.cardTitle}>General</Text>
          <View style={styles.settingRow}>
            <View>
              <Text style={{ color: 'white', fontSize: 16 }}>Auto-Speak</Text>
              <Text style={{ color: THEME.textSecondary, fontSize: 12 }}>TTS on detection</Text>
            </View>
            <Switch
              value={autoSpeak}
              onValueChange={setAutoSpeak}
              trackColor={{ false: '#333', true: THEME.primary }}
              thumbColor={'white'}
            />
          </View>
        </View>

        {/* LANGUAGE */}
        <View style={[styles.card, { marginTop: 16 }]}>
          <Text style={styles.cardTitle}>Target Language</Text>
          {languages.map(lang => (
            <TouchableOpacity
              key={lang.code}
              style={[
                styles.langItem,
                language === lang.code && { backgroundColor: 'rgba(230, 212, 143, 0.1)', borderColor: THEME.primary }
              ]}
              onPress={() => setLanguage(lang.code)}
            >
              <Text style={{ color: language === lang.code ? THEME.primary : 'white' }}>{lang.name}</Text>
              {language === lang.code && <Ionicons name="checkmark" color={THEME.primary} size={18} />}
            </TouchableOpacity>
          ))}
        </View>

      </ScrollView>
    </SafeAreaView>
  );
}

// --- MAIN APP ---

const Tab = createBottomTabNavigator();

export default function App() {
  const [ip, setIp] = useState('192.168.137.1'); // Hotspot Default
  const [isConnected, setIsConnected] = useState(false);
  const [gesture, setGesture] = useState('WAITING');
  const [sentence, setSentence] = useState('Waiting...');
  const [latency, setLatency] = useState(0);
  const [autoSpeak, setAutoSpeak] = useState(false);
  const [language, setLanguage] = useState('en');
  const [logs, setLogs] = useState([]);

  // Load Settings
  useEffect(() => {
    AsyncStorage.getItem('ip').then(val => val && setIp(val));
    AsyncStorage.getItem('lang').then(val => val && setLanguage(val));
  }, []);

  const addLog = (msg) => {
    const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    setLogs(prev => [{ id: Date.now(), message: msg, time }, ...prev].slice(0, 50));
  };

  const speak = (msg) => {
    if (!msg || msg === 'Waiting...') return;
    Speech.speak(msg, { language: language === 'en' ? 'en-US' : language });
  };

  // Poll Backend
  useEffect(() => {
    if (!isConnected) return;
    const interval = setInterval(() => {
      const start = Date.now();
      const controller = new AbortController();

      // Timeout protection
      setTimeout(() => controller.abort(), 2000);

      fetch(`http://${ip}:8000/imu?lang=${language}`, { signal: controller.signal })
        .then(res => res.json())
        .then(data => {
          setLatency(Date.now() - start);

          if (data.gesture && data.gesture !== 'WAITING') {
            if (data.gesture !== gesture) {
              setGesture(data.gesture);
              const txt = data.sentence || data.gesture;
              setSentence(txt);
              addLog(`Detected: ${data.gesture}`);

              if (autoSpeak) speak(txt);
            }
          }
        })
        .catch(() => { });
    }, 200);
    return () => clearInterval(interval);
  }, [isConnected, ip, language, gesture, autoSpeak]);

  const connect = () => {
    AsyncStorage.setItem('ip', ip);
    setIsConnected(true);
    addLog("Connected to Backend");
  };

  return (
    <SafeAreaProvider>
      <StatusBar barStyle="light-content" backgroundColor="#0B0B0B" />

      <ConnectionOverlay
        isConnected={isConnected}
        onConnect={connect}
        ip={ip} setIp={setIp}
        onDemo={() => setIsConnected(true)}
      />

      <NavigationContainer theme={{
        ...NavTheme,
        colors: { ...NavTheme.colors, background: THEME.bg }
      }}>
        <Tab.Navigator
          screenOptions={({ route }) => ({
            headerShown: false,
            tabBarStyle: styles.tabBar,
            tabBarActiveTintColor: THEME.primary,
            tabBarInactiveTintColor: THEME.textSecondary,
            tabBarIcon: ({ color, size }) => {
              let iconName;
              if (route.name === 'Dashboard') iconName = 'view-dashboard';
              else if (route.name === 'Analytics') iconName = 'chart-bar';
              else if (route.name === 'History') iconName = 'history';
              else if (route.name === 'Settings') iconName = 'cog';
              return <MaterialCommunityIcons name={iconName} size={size} color={color} />;
            },
          })}
        >
          <Tab.Screen name="Dashboard">
            {props => (
              <DashboardScreen
                {...props}
                gesture={gesture}
                sentence={sentence}
                latency={latency}
                autoSpeak={autoSpeak}
                speak={speak}
              />
            )}
          </Tab.Screen>

          <Tab.Screen name="Analytics" component={AnalyticsScreen} />

          <Tab.Screen name="History">
            {props => <HistoryScreen {...props} logs={logs} />}
          </Tab.Screen>

          <Tab.Screen name="Settings">
            {props => (
              <SettingsScreen
                {...props}
                ip={ip} setIp={setIp}
                autoSpeak={autoSpeak} setAutoSpeak={setAutoSpeak}
                language={language} setLanguage={setLanguage}
              />
            )}
          </Tab.Screen>
        </Tab.Navigator>
      </NavigationContainer>
    </SafeAreaProvider>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: THEME.bg },
  overlay: { ...StyleSheet.absoluteFillObject, backgroundColor: 'black', justifyContent: 'center' },
  content: { padding: 20, paddingBottom: 100 },

  // Text
  h1: { color: 'white', fontSize: 32, fontWeight: 'bold', marginBottom: 8 },
  subtitle: { color: THEME.textSecondary, fontSize: 16, marginBottom: 40 },
  header: { padding: 20, flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', borderBottomWidth: 1, borderBottomColor: THEME.border },
  headerTitle: { color: 'white', fontSize: 20, fontWeight: '600' },

  // Elements
  input: {
    width: '100%', backgroundColor: '#1A1A1A', color: 'white',
    padding: 16, borderRadius: 12, borderWidth: 1, borderColor: '#333',
    marginBottom: 20, fontSize: 16
  },
  btnPrimary: {
    width: '100%', backgroundColor: THEME.primary, padding: 16,
    borderRadius: 16, flexDirection: 'row', justifyContent: 'center', alignItems: 'center'
  },
  btnText: { color: 'black', fontWeight: 'bold', fontSize: 16 },

  // Cards
  heroCard: {
    padding: 24, borderRadius: 24, borderWidth: 1, borderColor: 'rgba(230, 212, 143, 0.1)',
    alignItems: 'center', minHeight: 180, justifyContent: 'center', marginTop: 20
  },
  card: {
    backgroundColor: THEME.card, padding: 24, borderRadius: 16,
    borderWidth: 1, borderColor: THEME.border
  },
  cardTitle: { color: THEME.textSecondary, fontSize: 14, fontWeight: '500' },
  heroText: { color: THEME.primary, fontSize: 48, fontWeight: 'bold', marginVertical: 20 },
  badge: { backgroundColor: 'rgba(255,255,255,0.05)', paddingHorizontal: 12, paddingVertical: 6, borderRadius: 20 },
  badgeText: { color: THEME.textSecondary, fontSize: 12 },
  sentenceText: { color: 'white', fontSize: 18, marginVertical: 16, lineHeight: 28 },

  // Layouts
  rowBetween: { flexDirection: 'row', justifyContent: 'space-between', width: '100%' },
  rowStart: { flexDirection: 'row', alignItems: 'center' },
  statusRow: { flexDirection: 'row', gap: 12, marginVertical: 24 },
  statCard: {
    flex: 1, backgroundColor: THEME.card, padding: 16, borderRadius: 12,
    alignItems: 'center', borderWidth: 1, borderColor: THEME.border
  },
  statLabel: { color: THEME.textSecondary, fontSize: 10, marginBottom: 4 },
  statValue: { color: 'white', fontWeight: 'bold', fontSize: 14 },

  // Charts
  chartContainer: { flexDirection: 'row', height: 120, alignItems: 'flex-end', justifyContent: 'space-between', marginTop: 16, gap: 8 },
  barContainer: { flex: 1, height: '100%', justifyContent: 'flex-end' },
  bar: { width: '100%', backgroundColor: THEME.primary, borderRadius: 4 },
  chartLegend: { color: THEME.textSecondary, fontSize: 12, textAlign: 'center', marginTop: 12 },

  // Logs
  logItem: {
    backgroundColor: THEME.card, padding: 16, borderRadius: 12, marginBottom: 8,
    flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center',
    borderWidth: 1, borderColor: THEME.border
  },

  // Settings
  settingRow: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginTop: 12 },
  langItem: {
    padding: 16, borderBottomWidth: 1, borderBottomColor: THEME.border,
    flexDirection: 'row', justifyContent: 'space-between'
  },
  avatar: {
    width: 36, height: 36, borderRadius: 18, backgroundColor: THEME.card,
    alignItems: 'center', justifyContent: 'center', borderWidth: 1, borderColor: '#333'
  },

  // Nav
  tabBar: {
    backgroundColor: 'rgba(30,30,30,0.95)', borderTopWidth: 0, height: 60,
    paddingBottom: 5, paddingTop: 5, position: 'absolute', bottom: 20,
    left: 20, right: 20, borderRadius: 30, elevation: 0
  }
});

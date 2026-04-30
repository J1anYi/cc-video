import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity, TVEventHandler } from 'react-native';

interface TVButtonProps {
  title: string;
  onPress: () => void;
  focused?: boolean;
  style?: any;
}

export function TVButton({ title, onPress, focused = false, style }: TVButtonProps) {
  const [isFocused, setIsFocused] = React.useState(focused);

  return (
    <TouchableOpacity
      activeOpacity={0.8}
      onPress={onPress}
      onFocus={() => setIsFocused(true)}
      onBlur={() => setIsFocused(false)}
      style={[
        styles.button,
        isFocused && styles.buttonFocused,
        style,
      ]}
      hasTVPreferredFocus={focused}
      isTVSelectable
    >
      <Text style={[styles.text, isFocused && styles.textFocused]}>{title}</Text>
    </TouchableOpacity>
  );
}

const styles = StyleSheet.create({
  button: {
    backgroundColor: '#1f1f1f',
    paddingVertical: 16,
    paddingHorizontal: 24,
    borderRadius: 8,
    margin: 8,
  },
  buttonFocused: {
    backgroundColor: '#e50914',
    transform: [{ scale: 1.1 }],
  },
  text: {
    color: '#fff',
    fontSize: 18,
    fontWeight: 'bold',
  },
  textFocused: {
    color: '#fff',
  },
});

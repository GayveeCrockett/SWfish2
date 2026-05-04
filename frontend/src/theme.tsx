import { createContext, useContext, useMemo, useState, ReactNode } from "react";

export type ThemeMode = "light" | "dark";

export type Theme = {
  mode: ThemeMode;
  bg: string;
  surface: string;
  surfaceHighlight: string;
  overlay: string;
  textPrimary: string;
  textSecondary: string;
  textInverse: string;
  placeholder: string;
  primary: string;
  primaryLight: string;
  secondary: string;
  yellow: string;
  coral: string;
  green: string;
  chipBorder: string;
  chipBg: string;
  cardShadow: string;
  statusBar: "light" | "dark";
};

export const LIGHT_THEME: Theme = {
  mode: "light",
  bg: "#F6FBFC",
  surface: "#FFFFFF",
  surfaceHighlight: "#E8F4F8",
  overlay: "rgba(3, 4, 94, 0.4)",
  textPrimary: "#03045E",
  textSecondary: "#5B8E9D",
  textInverse: "#FFFFFF",
  placeholder: "#8ECAE6",
  primary: "#0077B6",
  primaryLight: "#00B4D8",
  secondary: "#48CAE4",
  yellow: "#FFD166",
  coral: "#EF476F",
  green: "#06D6A0",
  chipBorder: "#00B4D8",
  chipBg: "#FFFFFF",
  cardShadow: "#0077B6",
  statusBar: "dark",
};

export const DARK_THEME: Theme = {
  mode: "dark",
  bg: "#061A2B",
  surface: "#0D2A44",
  surfaceHighlight: "#133A5E",
  overlay: "rgba(0, 0, 0, 0.65)",
  textPrimary: "#E6F4FA",
  textSecondary: "#8FB3C6",
  textInverse: "#061A2B",
  placeholder: "#4D7A91",
  primary: "#48CAE4",
  primaryLight: "#90E0EF",
  secondary: "#00B4D8",
  yellow: "#FFD166",
  coral: "#EF476F",
  green: "#06D6A0",
  chipBorder: "#48CAE4",
  chipBg: "#133A5E",
  cardShadow: "#000000",
  statusBar: "light",
};

type ThemeContextValue = {
  theme: Theme;
  toggle: () => void;
  setMode: (m: ThemeMode) => void;
};

const ThemeContext = createContext<ThemeContextValue | null>(null);

export function ThemeProvider({ children }: { children: ReactNode }) {
  const [mode, setMode] = useState<ThemeMode>("light");
  const value = useMemo<ThemeContextValue>(
    () => ({
      theme: mode === "light" ? LIGHT_THEME : DARK_THEME,
      toggle: () => setMode((m) => (m === "light" ? "dark" : "light")),
      setMode,
    }),
    [mode]
  );
  return <ThemeContext.Provider value={value}>{children}</ThemeContext.Provider>;
}

export function useTheme(): ThemeContextValue {
  const ctx = useContext(ThemeContext);
  if (!ctx) throw new Error("useTheme must be used within ThemeProvider");
  return ctx;
}

export const FONTS = {
  h1: { fontFamily: "Fredoka_600SemiBold", fontSize: 32, letterSpacing: 0.5 },
  h2: { fontFamily: "Fredoka_600SemiBold", fontSize: 24, letterSpacing: 0.25 },
  h3: { fontFamily: "Fredoka_500Medium", fontSize: 20 },
  bodyLg: { fontFamily: "Nunito_400Regular", fontSize: 18 },
  body: { fontFamily: "Nunito_400Regular", fontSize: 16 },
  bodyBold: { fontFamily: "Nunito_700Bold", fontSize: 16 },
  label: { fontFamily: "Nunito_700Bold", fontSize: 12, letterSpacing: 0.8, textTransform: "uppercase" as const },
  caption: { fontFamily: "Nunito_500Medium", fontSize: 12 },
};

export const SPACING = { xs: 4, sm: 8, md: 16, lg: 24, xl: 32 };
export const RADIUS = { sm: 8, md: 16, lg: 24, pill: 9999 };

export const COLOR_SWATCH: Record<string, string> = {
  orange: "#FF9F1C",
  yellow: "#FFD166",
  red: "#EF476F",
  pink: "#F4A5C0",
  purple: "#8338EC",
  blue: "#0077B6",
  green: "#06D6A0",
  black: "#1A1A2E",
  white: "#FFFFFF",
  brown: "#8B5E3C",
};

export const FRUIT_EMOJI: Record<string, string> = {
  banana: "🍌",
  mango: "🥭",
  kiwi: "🥝",
  strawberry: "🍓",
};

export const PLACEHOLDER_IMAGE =
  "https://images.pexels.com/photos/30570561/pexels-photo-30570561.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940";

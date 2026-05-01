export const COLORS = {
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
};

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

export const SHADOW_CARD = {
  shadowColor: "#0077B6",
  shadowOffset: { width: 0, height: 8 },
  shadowOpacity: 0.1,
  shadowRadius: 16,
  elevation: 4,
};

/** Map a color name from the fish dataset to a visual swatch hex. */
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

export const PLACEHOLDER_IMAGE =
  "https://images.pexels.com/photos/30570561/pexels-photo-30570561.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940";

import React, { useEffect, useMemo, useState } from "react";
import {
  View,
  Text,
  Image,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  ActivityIndicator,
} from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import { Ionicons } from "@expo/vector-icons";
import { useLocalSearchParams, useRouter } from "expo-router";
import { FONTS, SPACING, RADIUS, COLOR_SWATCH, SWSA_ICON, PLACEHOLDER_IMAGE, useTheme, Theme } from "../../src/theme";
import { fetchFish, Fish } from "../../src/api";

export default function FishDetail() {
  const { id } = useLocalSearchParams<{ id: string }>();
  const router = useRouter();
  const { theme } = useTheme();
  const [fish, setFish] = useState<Fish | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!id) return;
    setLoading(true);
    fetchFish(id)
      .then(setFish)
      .catch((e) => console.warn("fetchFish error", e))
      .finally(() => setLoading(false));
  }, [id]);

  const styles = useMemo(() => makeStyles(theme), [theme]);

  if (loading) {
    return (
      <View style={styles.center}>
        <ActivityIndicator color={theme.primary} size="large" />
      </View>
    );
  }
  if (!fish) {
    return (
      <SafeAreaView style={styles.center}>
        <Text style={FONTS.h2}>Fish not found</Text>
        <TouchableOpacity onPress={() => router.back()} style={styles.backTextBtn}>
          <Text style={{ ...FONTS.bodyBold, color: theme.primary }}>Go back</Text>
        </TouchableOpacity>
      </SafeAreaView>
    );
  }

  const edible = fish.can_eat?.toLowerCase().includes("technically");
  const poisonous = fish.poison_toxin === "yes";

  return (
    <View style={styles.container}>
      <View style={styles.heroWrap}>
        <Image source={{ uri: fish.image_url || PLACEHOLDER_IMAGE }} style={styles.hero} />
        <View style={styles.heroOverlay} />
      </View>

      <SafeAreaView style={styles.headerRow} edges={["top"]}>
        <TouchableOpacity testID="back-btn" onPress={() => router.back()} style={styles.backBtn}>
          <Ionicons name="chevron-back" size={24} color={theme.textPrimary} />
        </TouchableOpacity>
      </SafeAreaView>

      <ScrollView
        style={styles.sheet}
        contentContainerStyle={styles.sheetContent}
        showsVerticalScrollIndicator={false}
      >
        <View style={styles.titleBlock}>
          <Text style={styles.eyebrow}>
            {(fish.habitats[0] || "REEF").toUpperCase()} SPECIES
          </Text>
          <Text style={styles.title} testID="fish-name">{capitalize(fish.name)}</Text>

          <View style={styles.colorChipRow}>
            {fish.colors.map((c) => (
              <View key={c} style={styles.colorChip}>
                <View
                  style={[
                    styles.colorSwatch,
                    { backgroundColor: COLOR_SWATCH[c] || "#ccc", borderColor: c === "white" ? theme.surfaceHighlight : "transparent" },
                  ]}
                />
                <Text style={styles.colorChipText}>{c}</Text>
              </View>
            ))}
          </View>
        </View>

        <View style={styles.bentoGrid}>
          <StatCard theme={theme} label="Diet" value={fish.diet ? capitalize(fish.diet) : "Unknown"} icon="restaurant" tint={theme.green} />
          <StatCard theme={theme} label="Longevity" value={fish.longevity} icon="time" tint={theme.primaryLight} />
          <StatCard
            theme={theme}
            label="Conservation"
            value={fish.conservation_status}
            icon="leaf"
            tint={fish.conservation_status === "LC" ? theme.green : theme.yellow}
          />
          <StatCard
            theme={theme}
            label="Can I eat it?"
            value={fish.can_eat}
            icon={edible ? "checkmark-circle" : "close-circle"}
            tint={edible ? theme.yellow : theme.coral}
          />
        </View>

        <View style={[styles.banner, poisonous ? styles.bannerDanger : styles.bannerSafe]} testID="poison-banner">
          <Ionicons
            name={poisonous ? "warning" : "shield-checkmark"}
            size={22}
            color={poisonous ? "#fff" : theme.primary}
          />
          <View style={{ flex: 1, marginLeft: 10 }}>
            <Text style={[styles.bannerTitle, poisonous && { color: "#fff" }]}>
              {poisonous ? "Toxic / Venomous" : "Not known to be toxic"}
            </Text>
            <Text style={[styles.bannerBody, poisonous && { color: "#fff" }]}>
              {poisonous
                ? "Handle with care — this species can be harmful."
                : "Generally safe to observe and handle responsibly."}
            </Text>
          </View>
        </View>

        <Section theme={theme} title="Natural Habitat">
          <View style={styles.habRow}>
            {fish.habitats.map((h) => (
              <View key={h} style={styles.habPill}>
                <Ionicons name="location" size={14} color={theme.primary} />
                <Text style={styles.habPillText}>{h}</Text>
              </View>
            ))}
          </View>
          {fish.natural_hab_raw && fish.natural_hab_raw.toLowerCase() !== fish.habitats.join(", ").toLowerCase() && (
            <Text style={styles.bodyText}>Full range: {fish.natural_hab_raw}</Text>
          )}
        </Section>

        {fish.swsa_habitats && fish.swsa_habitats.length > 0 ? (
          <Section theme={theme} title="SWSA Habitat">
            <View style={styles.habRow}>
              {fish.swsa_habitats.map((h) => (
                <View key={h} style={styles.fruitPill} testID={`swsa-pill-${h}`}>
                  <Text style={styles.fruitPillEmoji}>{SWSA_ICON[h] || "🐟"}</Text>
                  <Text style={styles.fruitPillText}>{h}</Text>
                </View>
              ))}
            </View>
          </Section>
        ) : null}

        {fish.nifty_facts ? (
          <Section theme={theme} title="Nifty Fact">
            <View style={styles.factCard}>
              <Text style={styles.factEmoji}>✨</Text>
              <Text style={styles.factText}>{fish.nifty_facts}</Text>
            </View>
          </Section>
        ) : null}

        <Section theme={theme} title="Description">
          <Text style={styles.bodyText}>
            {fish.description
              ? `Known for its ${fish.description} coloring.`
              : "A striking reef-dweller with its own unique flair."}
          </Text>
        </Section>
      </ScrollView>
    </View>
  );
}

function StatCard({
  theme,
  label,
  value,
  icon,
  tint,
}: {
  theme: Theme;
  label: string;
  value: string;
  icon: React.ComponentProps<typeof Ionicons>["name"];
  tint: string;
}) {
  const styles = makeStyles(theme);
  return (
    <View style={styles.bento}>
      <View style={[styles.bentoIcon, { backgroundColor: tint + "22" }]}>
        <Ionicons name={icon} size={18} color={tint} />
      </View>
      <Text style={styles.bentoLabel}>{label}</Text>
      <Text style={styles.bentoValue} numberOfLines={1} adjustsFontSizeToFit minimumFontScale={0.7}>{value}</Text>
    </View>
  );
}

function Section({ theme, title, children }: { theme: Theme; title: string; children: React.ReactNode }) {
  const styles = makeStyles(theme);
  return (
    <View style={{ marginTop: SPACING.lg }}>
      <Text style={styles.sectionTitle}>{title}</Text>
      {children}
    </View>
  );
}

function capitalize(s: string) {
  if (!s) return "";
  return s.split(" ").map((w) => (w.length ? w[0].toUpperCase() + w.slice(1) : w)).join(" ");
}

const makeStyles = (t: Theme) =>
  StyleSheet.create({
    container: { flex: 1, backgroundColor: t.bg },
    center: { flex: 1, backgroundColor: t.bg, alignItems: "center", justifyContent: "center" },
    heroWrap: { position: "absolute", top: 0, left: 0, right: 0, height: 340 },
    hero: { width: "100%", height: "100%" },
    heroOverlay: { ...StyleSheet.absoluteFillObject, backgroundColor: t.mode === "dark" ? "rgba(0,0,0,0.45)" : "rgba(3,4,94,0.25)" },
    headerRow: { position: "absolute", top: 0, left: 0, right: 0, paddingHorizontal: SPACING.md },
    backBtn: {
      width: 44,
      height: 44,
      borderRadius: 22,
      backgroundColor: t.mode === "dark" ? t.surface : "rgba(255,255,255,0.92)",
      alignItems: "center",
      justifyContent: "center",
      marginTop: 8,
    },
    backTextBtn: { marginTop: 16 },

    sheet: { flex: 1, marginTop: 280 },
    sheetContent: {
      backgroundColor: t.bg,
      borderTopLeftRadius: 32,
      borderTopRightRadius: 32,
      padding: SPACING.lg,
      paddingBottom: 60,
      minHeight: "100%",
    },

    titleBlock: { marginBottom: SPACING.md },
    eyebrow: { ...FONTS.label, color: t.primaryLight },
    title: { ...FONTS.h1, color: t.textPrimary, marginTop: 4 },

    colorChipRow: { flexDirection: "row", flexWrap: "wrap", gap: 8, marginTop: 14 },
    colorChip: {
      flexDirection: "row",
      alignItems: "center",
      backgroundColor: t.surface,
      paddingHorizontal: 10,
      paddingVertical: 6,
      borderRadius: RADIUS.pill,
      borderWidth: 1,
      borderColor: t.surfaceHighlight,
    },
    colorSwatch: { width: 12, height: 12, borderRadius: 6, marginRight: 6, borderWidth: 1 },
    colorChipText: { ...FONTS.caption, color: t.textPrimary, fontFamily: "Nunito_700Bold" },

    bentoGrid: { flexDirection: "row", flexWrap: "wrap", gap: 12, marginTop: SPACING.md },
    bento: {
      width: "47%",
      flexGrow: 1,
      backgroundColor: t.surface,
      borderRadius: RADIUS.lg,
      padding: SPACING.md,
      shadowColor: t.cardShadow,
      shadowOffset: { width: 0, height: 8 },
      shadowOpacity: t.mode === "dark" ? 0.4 : 0.1,
      shadowRadius: 16,
      elevation: 4,
    },
    bentoIcon: { width: 32, height: 32, borderRadius: 16, alignItems: "center", justifyContent: "center", marginBottom: 8 },
    bentoLabel: { fontFamily: "Nunito_700Bold", fontSize: 11, letterSpacing: 0.6, textTransform: "uppercase", color: t.textSecondary, marginBottom: 2 },
    bentoValue: { fontFamily: "Fredoka_500Medium", fontSize: 16, color: t.textPrimary },

    banner: {
      flexDirection: "row",
      alignItems: "center",
      borderRadius: RADIUS.lg,
      padding: SPACING.md,
      marginTop: SPACING.lg,
    },
    bannerSafe: { backgroundColor: t.surfaceHighlight },
    bannerDanger: { backgroundColor: t.coral },
    bannerTitle: { ...FONTS.bodyBold, color: t.textPrimary },
    bannerBody: { ...FONTS.caption, color: t.textSecondary, marginTop: 2 },

    sectionTitle: { ...FONTS.h2, color: t.textPrimary, marginBottom: SPACING.sm },

    habRow: { flexDirection: "row", flexWrap: "wrap", gap: 8, marginBottom: 8 },
    habPill: {
      flexDirection: "row",
      alignItems: "center",
      gap: 4,
      paddingHorizontal: 12,
      paddingVertical: 6,
      backgroundColor: t.surface,
      borderRadius: RADIUS.pill,
      borderWidth: 1,
      borderColor: t.surfaceHighlight,
    },
    habPillText: { ...FONTS.caption, color: t.textPrimary, fontFamily: "Nunito_700Bold" },

    fruitPill: {
      flexDirection: "row",
      alignItems: "center",
      gap: 6,
      paddingHorizontal: 14,
      paddingVertical: 8,
      backgroundColor: t.yellow + "33",
      borderRadius: RADIUS.pill,
      borderWidth: 1.5,
      borderColor: t.yellow,
    },
    fruitPillEmoji: { fontSize: 18 },
    fruitPillText: { ...FONTS.bodyBold, color: t.textPrimary },

    factCard: {
      flexDirection: "row",
      alignItems: "flex-start",
      backgroundColor: t.yellow + "33",
      borderRadius: RADIUS.lg,
      padding: SPACING.md,
      borderWidth: 1,
      borderColor: t.yellow,
    },
    factEmoji: { fontSize: 22, marginRight: 10 },
    factText: { ...FONTS.body, color: t.textPrimary, flex: 1 },

    bodyText: { ...FONTS.body, color: t.textSecondary, lineHeight: 22 },
  });

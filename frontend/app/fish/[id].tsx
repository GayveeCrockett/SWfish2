import React, { useEffect, useState } from "react";
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
import { COLORS, FONTS, SPACING, RADIUS, SHADOW_CARD, COLOR_SWATCH, PLACEHOLDER_IMAGE } from "../../src/theme";
import { fetchFish, Fish } from "../../src/api";

export default function FishDetail() {
  const { id } = useLocalSearchParams<{ id: string }>();
  const router = useRouter();
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

  if (loading) {
    return (
      <View style={styles.center}>
        <ActivityIndicator color={COLORS.primary} size="large" />
      </View>
    );
  }
  if (!fish) {
    return (
      <SafeAreaView style={styles.center}>
        <Text style={FONTS.h2}>Fish not found</Text>
        <TouchableOpacity onPress={() => router.back()} style={styles.backTextBtn}>
          <Text style={{ ...FONTS.bodyBold, color: COLORS.primary }}>Go back</Text>
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
          <Ionicons name="chevron-back" size={24} color={COLORS.textPrimary} />
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
                    { backgroundColor: COLOR_SWATCH[c] || "#ccc", borderColor: c === "white" ? "#E8F4F8" : "transparent" },
                  ]}
                />
                <Text style={styles.colorChipText}>{c}</Text>
              </View>
            ))}
          </View>
        </View>

        <View style={styles.bentoGrid}>
          <StatCard label="Diet" value={fish.diet ? capitalize(fish.diet) : "Unknown"} icon="restaurant" tint={COLORS.green} />
          <StatCard label="Longevity" value={fish.longevity} icon="time" tint={COLORS.primaryLight} />
          <StatCard
            label="Conservation"
            value={fish.conservation_status}
            icon="leaf"
            tint={fish.conservation_status === "LC" ? COLORS.green : COLORS.yellow}
          />
          <StatCard
            label="Can I eat it?"
            value={fish.can_eat}
            icon={edible ? "checkmark-circle" : "close-circle"}
            tint={edible ? COLORS.yellow : COLORS.coral}
          />
        </View>

        <View style={[styles.banner, poisonous ? styles.bannerDanger : styles.bannerSafe]} testID="poison-banner">
          <Ionicons
            name={poisonous ? "warning" : "shield-checkmark"}
            size={22}
            color={poisonous ? "#fff" : COLORS.primary}
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

        <Section title="Natural Habitat">
          <View style={styles.habRow}>
            {fish.habitats.map((h) => (
              <View key={h} style={styles.habPill}>
                <Ionicons name="location" size={14} color={COLORS.primary} />
                <Text style={styles.habPillText}>{h}</Text>
              </View>
            ))}
          </View>
          {fish.natural_hab_raw && fish.natural_hab_raw.toLowerCase() !== fish.habitats.join(", ").toLowerCase() && (
            <Text style={styles.bodyText}>Full range: {fish.natural_hab_raw}</Text>
          )}
        </Section>

        {fish.nifty_facts ? (
          <Section title="Nifty Fact">
            <View style={styles.factCard}>
              <Text style={styles.factEmoji}>✨</Text>
              <Text style={styles.factText}>{fish.nifty_facts}</Text>
            </View>
          </Section>
        ) : null}

        <Section title="Description">
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
  label,
  value,
  icon,
  tint,
}: {
  label: string;
  value: string;
  icon: React.ComponentProps<typeof Ionicons>["name"];
  tint: string;
}) {
  return (
    <View style={styles.bento}>
      <View style={[styles.bentoIcon, { backgroundColor: tint + "22" }]}>
        <Ionicons name={icon} size={18} color={tint} />
      </View>
      <Text style={styles.bentoLabel}>{label}</Text>
      <Text style={styles.bentoValue} numberOfLines={2}>{value}</Text>
    </View>
  );
}

function Section({ title, children }: { title: string; children: React.ReactNode }) {
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

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: COLORS.bg },
  center: { flex: 1, backgroundColor: COLORS.bg, alignItems: "center", justifyContent: "center" },
  heroWrap: { position: "absolute", top: 0, left: 0, right: 0, height: 340 },
  hero: { width: "100%", height: "100%" },
  heroOverlay: { ...StyleSheet.absoluteFillObject, backgroundColor: "rgba(3,4,94,0.25)" },
  headerRow: { position: "absolute", top: 0, left: 0, right: 0, paddingHorizontal: SPACING.md },
  backBtn: {
    width: 44,
    height: 44,
    borderRadius: 22,
    backgroundColor: "rgba(255,255,255,0.92)",
    alignItems: "center",
    justifyContent: "center",
    marginTop: 8,
  },
  backTextBtn: { marginTop: 16 },

  sheet: { flex: 1, marginTop: 280 },
  sheetContent: {
    backgroundColor: COLORS.bg,
    borderTopLeftRadius: 32,
    borderTopRightRadius: 32,
    padding: SPACING.lg,
    paddingBottom: 60,
    minHeight: "100%",
  },

  titleBlock: { marginBottom: SPACING.md },
  eyebrow: { ...FONTS.label, color: COLORS.primaryLight },
  title: { ...FONTS.h1, color: COLORS.textPrimary, marginTop: 4 },

  colorChipRow: { flexDirection: "row", flexWrap: "wrap", gap: 8, marginTop: 14 },
  colorChip: {
    flexDirection: "row",
    alignItems: "center",
    backgroundColor: COLORS.surface,
    paddingHorizontal: 10,
    paddingVertical: 6,
    borderRadius: RADIUS.pill,
    borderWidth: 1,
    borderColor: COLORS.surfaceHighlight,
  },
  colorSwatch: { width: 12, height: 12, borderRadius: 6, marginRight: 6, borderWidth: 1 },
  colorChipText: { ...FONTS.caption, color: COLORS.textPrimary, fontFamily: "Nunito_700Bold" },

  bentoGrid: { flexDirection: "row", flexWrap: "wrap", gap: 12, marginTop: SPACING.md },
  bento: {
    width: "47%",
    flexGrow: 1,
    backgroundColor: COLORS.surface,
    borderRadius: RADIUS.lg,
    padding: SPACING.md,
    ...SHADOW_CARD,
  },
  bentoIcon: { width: 36, height: 36, borderRadius: 18, alignItems: "center", justifyContent: "center", marginBottom: 10 },
  bentoLabel: { ...FONTS.label, color: COLORS.textSecondary, marginBottom: 2 },
  bentoValue: { ...FONTS.h3, color: COLORS.textPrimary },

  banner: {
    flexDirection: "row",
    alignItems: "center",
    borderRadius: RADIUS.lg,
    padding: SPACING.md,
    marginTop: SPACING.lg,
  },
  bannerSafe: { backgroundColor: COLORS.surfaceHighlight },
  bannerDanger: { backgroundColor: COLORS.coral },
  bannerTitle: { ...FONTS.bodyBold, color: COLORS.textPrimary },
  bannerBody: { ...FONTS.caption, color: COLORS.textSecondary, marginTop: 2 },

  sectionTitle: { ...FONTS.h2, color: COLORS.textPrimary, marginBottom: SPACING.sm },

  habRow: { flexDirection: "row", flexWrap: "wrap", gap: 8, marginBottom: 8 },
  habPill: {
    flexDirection: "row",
    alignItems: "center",
    gap: 4,
    paddingHorizontal: 12,
    paddingVertical: 6,
    backgroundColor: COLORS.surface,
    borderRadius: RADIUS.pill,
    borderWidth: 1,
    borderColor: COLORS.surfaceHighlight,
  },
  habPillText: { ...FONTS.caption, color: COLORS.textPrimary, fontFamily: "Nunito_700Bold" },

  factCard: {
    flexDirection: "row",
    alignItems: "flex-start",
    backgroundColor: COLORS.yellow + "33",
    borderRadius: RADIUS.lg,
    padding: SPACING.md,
    borderWidth: 1,
    borderColor: COLORS.yellow,
  },
  factEmoji: { fontSize: 22, marginRight: 10 },
  factText: { ...FONTS.body, color: COLORS.textPrimary, flex: 1 },

  bodyText: { ...FONTS.body, color: COLORS.textSecondary, lineHeight: 22 },
});

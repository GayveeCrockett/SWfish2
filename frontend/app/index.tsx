import React, { useCallback, useEffect, useMemo, useState } from "react";
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  FlatList,
  StyleSheet,
  Image,
  ActivityIndicator,
  ScrollView,
  Modal,
  Pressable,
  KeyboardAvoidingView,
  Platform,
} from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import { Ionicons } from "@expo/vector-icons";
import { useRouter } from "expo-router";
import {
  FONTS,
  SPACING,
  RADIUS,
  COLOR_SWATCH,
  FRUIT_EMOJI,
  PLACEHOLDER_IMAGE,
  useTheme,
  Theme,
} from "../src/theme";
import { fetchFilters, fetchFishes, Fish, FilterOptions, SearchFilters } from "../src/api";

const DEBOUNCE_MS = 300;

export default function Home() {
  const router = useRouter();
  const { theme, toggle } = useTheme();
  const [query, setQuery] = useState("");
  const [filters, setFilters] = useState<SearchFilters>({});
  const [options, setOptions] = useState<FilterOptions | null>(null);
  const [fishes, setFishes] = useState<Fish[]>([]);
  const [loading, setLoading] = useState(true);
  const [filterOpen, setFilterOpen] = useState(false);

  useEffect(() => {
    fetchFilters()
      .then(setOptions)
      .catch((e) => console.warn("filter options error", e));
  }, []);

  useEffect(() => {
    const t = setTimeout(() => {
      setLoading(true);
      fetchFishes({ ...filters, q: query.trim() || undefined })
        .then((res) => setFishes(res.fishes))
        .catch((e) => console.warn("fishes error", e))
        .finally(() => setLoading(false));
    }, DEBOUNCE_MS);
    return () => clearTimeout(t);
  }, [query, filters]);

  const activeFilterCount = useMemo(() => {
    const keys: (keyof SearchFilters)[] = ["colors", "diets", "habitats", "swsa_habitats", "conservation", "can_eat", "poison"];
    return keys.reduce((sum, k) => sum + ((filters[k] as string[] | undefined)?.length || 0), 0);
  }, [filters]);

  const clearAll = useCallback(() => {
    setFilters({});
    setQuery("");
  }, []);

  const styles = useMemo(() => makeStyles(theme), [theme]);

  const renderFish = useCallback(
    ({ item }: { item: Fish }) => (
      <TouchableOpacity
        testID={`fish-card-${item.id}`}
        style={styles.card}
        onPress={() => router.push(`/fish/${item.id}`)}
        activeOpacity={0.85}
      >
        <View style={styles.cardImageWrap}>
          <Image source={{ uri: item.image_url || PLACEHOLDER_IMAGE }} style={styles.cardImage} />
          <View style={styles.imageOverlay} />
          {item.poison_toxin === "yes" && (
            <View style={styles.poisonBadge} testID={`poison-badge-${item.id}`}>
              <Ionicons name="warning" size={12} color="#fff" />
              <Text style={styles.poisonBadgeText}>Toxic</Text>
            </View>
          )}
          {item.swsa_fruit && (
            <View style={styles.fruitBadge}>
              <Text style={styles.fruitEmoji}>{FRUIT_EMOJI[item.swsa_fruit] || "🐟"}</Text>
            </View>
          )}
        </View>
        <View style={styles.cardBody}>
          <Text style={styles.cardTitle} numberOfLines={1}>{capitalize(item.name)}</Text>
          <Text style={styles.cardMeta} numberOfLines={1}>
            {item.diet ? capitalize(item.diet) : "Unknown diet"} · {item.habitats[0] || "Unknown habitat"}
          </Text>
          <View style={styles.colorRow}>
            {item.colors.slice(0, 5).map((c) => (
              <View
                key={c}
                style={[styles.colorDot, { backgroundColor: COLOR_SWATCH[c] || "#ccc", borderColor: c === "white" ? theme.surfaceHighlight : "transparent" }]}
              />
            ))}
          </View>
        </View>
      </TouchableOpacity>
    ),
    [router, styles, theme]
  );

  return (
    <SafeAreaView style={styles.safe} edges={["top"]}>
      <KeyboardAvoidingView
        style={{ flex: 1 }}
        behavior={Platform.OS === "ios" ? "padding" : undefined}
      >
        <View style={styles.header}>
          <View style={styles.headerRow}>
            <View style={{ flex: 1 }}>
              <Text style={styles.eyebrow}>SEA WORLD SAN ANTONIO</Text>
              <Text style={styles.title}>Explorer&apos;s Reef</Text>
              <Text style={styles.subtitle}>{fishes.length} species · from clownfish to koi</Text>
            </View>
            <TouchableOpacity
              testID="theme-toggle-btn"
              onPress={toggle}
              style={styles.themeBtn}
              activeOpacity={0.8}
            >
              <Ionicons
                name={theme.mode === "light" ? "moon" : "sunny"}
                size={20}
                color={theme.primary}
              />
            </TouchableOpacity>
          </View>
        </View>

        <View style={styles.searchRow}>
          <View style={styles.searchBar}>
            <Ionicons name="search" size={20} color={theme.primaryLight} />
            <TextInput
              testID="search-input"
              style={styles.searchInput}
              placeholder="Search by fish name..."
              placeholderTextColor={theme.placeholder}
              value={query}
              onChangeText={setQuery}
              returnKeyType="search"
              autoCorrect={false}
            />
            {query.length > 0 && (
              <TouchableOpacity testID="clear-search-btn" onPress={() => setQuery("")}>
                <Ionicons name="close-circle" size={20} color={theme.textSecondary} />
              </TouchableOpacity>
            )}
          </View>
          <TouchableOpacity
            testID="open-filters-btn"
            style={styles.filterBtn}
            onPress={() => setFilterOpen(true)}
            activeOpacity={0.8}
          >
            <Ionicons name="options" size={22} color="#fff" />
            {activeFilterCount > 0 && (
              <View style={styles.filterBadge}>
                <Text style={styles.filterBadgeText}>{activeFilterCount}</Text>
              </View>
            )}
          </TouchableOpacity>
        </View>

        {activeFilterCount > 0 && (
          <TouchableOpacity testID="clear-all-filters" onPress={clearAll} style={styles.clearAllRow}>
            <Ionicons name="close" size={14} color={theme.coral} />
            <Text style={styles.clearAllText}>Clear {activeFilterCount} filter{activeFilterCount > 1 ? "s" : ""}</Text>
          </TouchableOpacity>
        )}

        {loading ? (
          <View style={styles.center}>
            <ActivityIndicator size="large" color={theme.primary} />
          </View>
        ) : fishes.length === 0 ? (
          <View style={styles.center} testID="empty-state">
            <Text style={styles.emptyEmoji}>🐟</Text>
            <Text style={styles.emptyTitle}>No fish found</Text>
            <Text style={styles.emptyBody}>Try adjusting your filters or search term.</Text>
          </View>
        ) : (
          <FlatList
            data={fishes}
            keyExtractor={(f) => f.id}
            renderItem={renderFish}
            numColumns={2}
            columnWrapperStyle={styles.colWrap}
            contentContainerStyle={styles.listContent}
            showsVerticalScrollIndicator={false}
            testID="fish-list"
          />
        )}

        {options && (
          <FilterSheet
            visible={filterOpen}
            onClose={() => setFilterOpen(false)}
            options={options}
            filters={filters}
            setFilters={setFilters}
            onClear={clearAll}
            theme={theme}
          />
        )}
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
}

function FilterSheet({
  visible,
  onClose,
  options,
  filters,
  setFilters,
  onClear,
  theme,
}: {
  visible: boolean;
  onClose: () => void;
  options: FilterOptions;
  filters: SearchFilters;
  setFilters: (f: SearchFilters) => void;
  onClear: () => void;
  theme: Theme;
}) {
  const styles = useMemo(() => makeStyles(theme), [theme]);

  const toggle = (key: keyof SearchFilters, val: string) => {
    const current = (filters[key] as string[] | undefined) || [];
    const next = current.includes(val) ? current.filter((x) => x !== val) : [...current, val];
    setFilters({ ...filters, [key]: next.length ? next : undefined });
  };

  const renderGroup = (
    label: string,
    key: keyof SearchFilters,
    values: string[],
    variant: "default" | "color" | "fruit" = "default"
  ) => {
    const active = (filters[key] as string[] | undefined) || [];
    return (
      <View style={styles.group}>
        <Text style={styles.groupLabel}>{label}</Text>
        <View style={styles.chipWrap}>
          {values.map((v) => {
            const isActive = active.includes(v);
            return (
              <TouchableOpacity
                key={v}
                testID={`filter-${String(key)}-${v}`}
                onPress={() => toggle(key, v)}
                style={[styles.chip, isActive && styles.chipActive]}
                activeOpacity={0.8}
              >
                {variant === "color" && (
                  <View
                    style={[
                      styles.chipSwatch,
                      { backgroundColor: COLOR_SWATCH[v] || "#ccc", borderColor: v === "white" ? "#ccc" : "transparent" },
                    ]}
                  />
                )}
                {variant === "fruit" && (
                  <Text style={styles.chipFruit}>{FRUIT_EMOJI[v] || ""}</Text>
                )}
                <Text style={[styles.chipText, isActive && styles.chipTextActive]}>{capitalize(v)}</Text>
              </TouchableOpacity>
            );
          })}
        </View>
      </View>
    );
  };

  return (
    <Modal visible={visible} animationType="slide" transparent onRequestClose={onClose}>
      <Pressable style={styles.modalBackdrop} onPress={onClose} />
      <View style={styles.sheet}>
        <View style={styles.sheetHandle} />
        <View style={styles.sheetHeader}>
          <Text style={styles.sheetTitle}>Filters</Text>
          <TouchableOpacity testID="reset-filters" onPress={onClear}>
            <Text style={styles.resetText}>Reset</Text>
          </TouchableOpacity>
        </View>
        <ScrollView showsVerticalScrollIndicator={false} contentContainerStyle={{ paddingBottom: 40 }}>
          {renderGroup("Color", "colors", options.colors, "color")}
          {renderGroup("Diet", "diets", options.diets)}
          {renderGroup("Natural Habitat", "habitats", options.habitats)}
          {renderGroup("SWSA Habitat", "swsa_habitats", options.swsa_habitats, "fruit")}
          {renderGroup("Conservation", "conservation", options.conservation)}
          {renderGroup("Can I eat that?", "can_eat", options.can_eat)}
          {renderGroup("Poison / Toxin", "poison", options.poison)}
        </ScrollView>
        <TouchableOpacity testID="apply-filters-btn" style={styles.applyBtn} onPress={onClose} activeOpacity={0.9}>
          <Text style={styles.applyBtnText}>Show Results</Text>
        </TouchableOpacity>
      </View>
    </Modal>
  );
}

function capitalize(s: string) {
  if (!s) return "";
  return s
    .split(" ")
    .map((w) => (w.length ? w[0].toUpperCase() + w.slice(1) : w))
    .join(" ");
}

const makeStyles = (t: Theme) =>
  StyleSheet.create({
    safe: { flex: 1, backgroundColor: t.bg },
    header: { paddingHorizontal: SPACING.lg, paddingTop: SPACING.md, paddingBottom: SPACING.sm },
    headerRow: { flexDirection: "row", alignItems: "center" },
    themeBtn: {
      width: 44,
      height: 44,
      borderRadius: 22,
      backgroundColor: t.surface,
      alignItems: "center",
      justifyContent: "center",
      borderWidth: 1.5,
      borderColor: t.surfaceHighlight,
    },
    eyebrow: { ...FONTS.label, color: t.primaryLight },
    title: { ...FONTS.h1, color: t.textPrimary, marginTop: 4 },
    subtitle: { ...FONTS.body, color: t.textSecondary, marginTop: 4 },

    searchRow: {
      flexDirection: "row",
      alignItems: "center",
      paddingHorizontal: SPACING.lg,
      marginTop: SPACING.md,
      gap: 10,
    },
    searchBar: {
      flex: 1,
      flexDirection: "row",
      alignItems: "center",
      backgroundColor: t.surface,
      borderRadius: RADIUS.pill,
      paddingHorizontal: 18,
      paddingVertical: 12,
      borderWidth: 2,
      borderColor: t.surfaceHighlight,
    },
    searchInput: { flex: 1, marginLeft: 10, ...FONTS.body, color: t.textPrimary, paddingVertical: 0 },
    filterBtn: {
      width: 48,
      height: 48,
      borderRadius: RADIUS.pill,
      backgroundColor: t.primary,
      alignItems: "center",
      justifyContent: "center",
      shadowColor: t.primaryLight,
      shadowOffset: { width: 0, height: 4 },
      shadowOpacity: 0.25,
      shadowRadius: 8,
      elevation: 4,
    },
    filterBadge: {
      position: "absolute",
      top: -4,
      right: -4,
      minWidth: 20,
      height: 20,
      borderRadius: 10,
      backgroundColor: t.coral,
      paddingHorizontal: 4,
      alignItems: "center",
      justifyContent: "center",
    },
    filterBadgeText: { color: "#fff", fontFamily: "Nunito_700Bold", fontSize: 11 },

    clearAllRow: {
      flexDirection: "row",
      alignItems: "center",
      alignSelf: "flex-start",
      gap: 4,
      paddingHorizontal: SPACING.lg,
      marginTop: 10,
    },
    clearAllText: { ...FONTS.caption, color: t.coral, fontFamily: "Nunito_700Bold" },

    listContent: { paddingHorizontal: SPACING.md, paddingTop: SPACING.md, paddingBottom: 40 },
    colWrap: { gap: SPACING.md, marginBottom: SPACING.md, paddingHorizontal: SPACING.xs },

    card: {
      flex: 1,
      backgroundColor: t.surface,
      borderRadius: RADIUS.lg,
      overflow: "hidden",
      shadowColor: t.cardShadow,
      shadowOffset: { width: 0, height: 8 },
      shadowOpacity: t.mode === "dark" ? 0.4 : 0.1,
      shadowRadius: 16,
      elevation: 4,
    },
    cardImageWrap: { height: 130, backgroundColor: t.surfaceHighlight },
    cardImage: { width: "100%", height: "100%" },
    imageOverlay: { ...StyleSheet.absoluteFillObject, backgroundColor: t.mode === "dark" ? "rgba(0,0,0,0.15)" : "rgba(0,119,182,0.08)" },
    poisonBadge: {
      position: "absolute",
      top: 8,
      right: 8,
      backgroundColor: t.coral,
      paddingHorizontal: 8,
      paddingVertical: 3,
      borderRadius: RADIUS.pill,
      flexDirection: "row",
      alignItems: "center",
      gap: 3,
    },
    poisonBadgeText: { color: "#fff", fontSize: 10, fontFamily: "Nunito_700Bold" },
    fruitBadge: {
      position: "absolute",
      top: 8,
      left: 8,
      width: 28,
      height: 28,
      borderRadius: 14,
      backgroundColor: "rgba(255,255,255,0.92)",
      alignItems: "center",
      justifyContent: "center",
    },
    fruitEmoji: { fontSize: 16 },
    cardBody: { padding: 12 },
    cardTitle: { ...FONTS.h3, color: t.textPrimary },
    cardMeta: { ...FONTS.caption, color: t.textSecondary, marginTop: 2 },
    colorRow: { flexDirection: "row", gap: 6, marginTop: 10 },
    colorDot: { width: 14, height: 14, borderRadius: 7, borderWidth: 1 },

    center: { flex: 1, alignItems: "center", justifyContent: "center", padding: SPACING.lg },
    emptyEmoji: { fontSize: 56, marginBottom: 12 },
    emptyTitle: { ...FONTS.h2, color: t.textPrimary },
    emptyBody: { ...FONTS.body, color: t.textSecondary, marginTop: 6, textAlign: "center" },

    modalBackdrop: { flex: 1, backgroundColor: t.overlay },
    sheet: {
      position: "absolute",
      left: 0,
      right: 0,
      bottom: 0,
      maxHeight: "85%",
      backgroundColor: t.bg,
      borderTopLeftRadius: 32,
      borderTopRightRadius: 32,
      paddingHorizontal: SPACING.lg,
      paddingTop: 10,
      paddingBottom: 20,
    },
    sheetHandle: { width: 44, height: 5, borderRadius: 3, backgroundColor: t.surfaceHighlight, alignSelf: "center", marginBottom: 12 },
    sheetHeader: { flexDirection: "row", justifyContent: "space-between", alignItems: "center", marginBottom: SPACING.md },
    sheetTitle: { ...FONTS.h2, color: t.textPrimary },
    resetText: { ...FONTS.bodyBold, color: t.coral },
    group: { marginBottom: SPACING.lg },
    groupLabel: { ...FONTS.label, color: t.textSecondary, marginBottom: 10 },
    chipWrap: { flexDirection: "row", flexWrap: "wrap", gap: 8 },
    chip: {
      flexDirection: "row",
      alignItems: "center",
      paddingHorizontal: 14,
      paddingVertical: 8,
      borderRadius: RADIUS.pill,
      borderWidth: 1.5,
      borderColor: t.chipBorder,
      backgroundColor: t.chipBg,
    },
    chipActive: { backgroundColor: t.primary, borderColor: t.primary },
    chipText: { ...FONTS.caption, color: t.textPrimary, fontFamily: "Nunito_700Bold" },
    chipTextActive: { color: t.mode === "dark" ? "#061A2B" : "#fff" },
    chipSwatch: { width: 12, height: 12, borderRadius: 6, marginRight: 6, borderWidth: 1 },
    chipFruit: { marginRight: 6, fontSize: 14 },
    applyBtn: {
      backgroundColor: t.primary,
      borderRadius: RADIUS.pill,
      paddingVertical: 16,
      alignItems: "center",
      marginTop: 8,
      shadowColor: t.primary,
      shadowOffset: { width: 0, height: 4 },
      shadowOpacity: 0.3,
      shadowRadius: 8,
      elevation: 5,
    },
    applyBtnText: { color: t.mode === "dark" ? "#061A2B" : "#fff", fontFamily: "Fredoka_600SemiBold", fontSize: 17, letterSpacing: 0.3 },
  });

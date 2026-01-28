import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

class AppTheme {
  // ─── Colors ────────────────────────────────────────────────────────────────
  // Primary: Deep Forest Green (Expertise, Growth)
  static const Color primaryGreen = Color(0xFF1B5E20); 
  static const Color darkGreen = Color(0xFF0D3312);
  
  // Accent: Gold (Premium Quality, Vanilla)
  static const Color accentGold = Color(0xFFD4AF37);
  static const Color lightGold = Color(0xFFFFE082);

  // Neutrals: Earthy & Natural
  static const Color backgroundCream = Color(0xFFF9F9F5); // Warm off-white
  static const Color surfaceWhite = Color(0xFFFFFFFF);
  static const Color textDark = Color(0xFF2D2D2D); // Soft black
  static const Color textGrey = Color(0xFF6D6D6D);
  
  // Status
  static const Color errorRed = Color(0xFFD32F2F);
  static const Color successGreen = Color(0xFF388E3C);

  // ─── Text Styles ───────────────────────────────────────────────────────────
  static TextTheme textTheme = GoogleFonts.outfitTextTheme().copyWith(
    displayLarge: GoogleFonts.playfairDisplay(
      fontSize: 32, fontWeight: FontWeight.bold, color: textDark, letterSpacing: -0.5
    ),
    displayMedium: GoogleFonts.playfairDisplay(
      fontSize: 28, fontWeight: FontWeight.bold, color: textDark
    ),
    headlineMedium: GoogleFonts.outfit(
      fontSize: 20, fontWeight: FontWeight.w600, color: textDark
    ),
    bodyLarge: GoogleFonts.outfit(
      fontSize: 16, color: textDark
    ),
    bodyMedium: GoogleFonts.outfit(
      fontSize: 14, color: textGrey
    ),
    labelLarge: GoogleFonts.outfit(
      fontSize: 14, fontWeight: FontWeight.bold, color: Colors.white, letterSpacing: 1.0
    ),
  );

  // ─── Theme Data ────────────────────────────────────────────────────────────
  static ThemeData get lightTheme {
    return ThemeData(
      useMaterial3: true,
      colorScheme: ColorScheme(
        brightness: Brightness.light,
        primary: primaryGreen,
        onPrimary: Colors.white,
        secondary: accentGold,
        onSecondary: Colors.black,
        error: errorRed,
        onError: Colors.white,
        background: backgroundCream,
        onBackground: textDark,
        surface: surfaceWhite,
        onSurface: textDark,
      ),
      scaffoldBackgroundColor: backgroundCream,
      textTheme: textTheme,
      
      // Card Theme
      cardTheme: CardThemeData(
        color: surfaceWhite,
        elevation: 0,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(16),
          side: BorderSide(color: Colors.grey.withOpacity(0.1))
        ),
      ),

      // Input Decoration
      inputDecorationTheme: InputDecorationTheme(
        filled: true,
        fillColor: surfaceWhite,
        contentPadding: const EdgeInsets.symmetric(horizontal: 20, vertical: 16),
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(12),
          borderSide: BorderSide(color: Colors.grey.withOpacity(0.2)),
        ),
        enabledBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(12),
          borderSide: BorderSide(color: Colors.grey.withOpacity(0.2)),
        ),
        focusedBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(12),
          borderSide: const BorderSide(color: primaryGreen, width: 2),
        ),
        labelStyle: const TextStyle(color: textGrey),
        prefixIconColor: primaryGreen,
      ),

      // Button Theme
      elevatedButtonTheme: ElevatedButtonThemeData(
        style: ElevatedButton.styleFrom(
          backgroundColor: primaryGreen,
          foregroundColor: Colors.white,
          elevation: 4,
          shadowColor: primaryGreen.withOpacity(0.4),
          padding: const EdgeInsets.symmetric(vertical: 16, horizontal: 24),
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
          textStyle: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
        ),
      ),
      
      // Floating Action Button
      floatingActionButtonTheme: const FloatingActionButtonThemeData(
        backgroundColor: accentGold,
        foregroundColor: darkGreen,
        elevation: 6,
      ),

      // AppBar Theme
      appBarTheme: const AppBarTheme(
        backgroundColor: backgroundCream,
        foregroundColor: textDark,
        elevation: 0,
        centerTitle: false,
        iconTheme: IconThemeData(color: primaryGreen),
      ),
    );
  }
}

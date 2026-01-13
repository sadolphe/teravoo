import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'screens/login_screen.dart';
import 'screens/home_screen.dart';

void main() {
  runApp(const TeraVooApp());
}

class TeraVooApp extends StatelessWidget {
  const TeraVooApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'TeraVoo Producer',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(
          seedColor: const Color(0xFF1B5E20), // Forest Green
          secondary: const Color(0xFFD4AF37), // Goldish
          background: const Color(0xFFF9F9F9), // Creamy
        ),
        useMaterial3: true,
        textTheme: GoogleFonts.outfitTextTheme(),
      ),
      initialRoute: '/login',
      routes: {
        '/login': (context) => const LoginScreen(),
        '/home': (context) => const HomeScreen(),
      },
      debugShowCheckedModeBanner: false,
    );
  }
}

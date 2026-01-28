import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'core/theme.dart';
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
      theme: AppTheme.lightTheme,
      initialRoute: '/login',
      routes: {
        '/login': (context) => const LoginScreen(),
        '/home': (context) => const HomeScreen(),
      },
      debugShowCheckedModeBanner: false,
    );
  }
}

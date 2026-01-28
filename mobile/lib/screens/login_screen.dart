import 'dart:ui';
import 'package:flutter/material.dart';
import '../core/api_client.dart';
import '../core/theme.dart';

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final TextEditingController _phoneController = TextEditingController();
  final TextEditingController _otpController = TextEditingController();
  bool _isLoading = false;
  bool _otpSent = false;
  final ApiClient _apiClient = ApiClient();

  Future<void> _handleSendOtp() async {
    if (_phoneController.text.isEmpty) {
      if (mounted) {
         ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(content: Text('Please enter a phone number'), backgroundColor: Colors.orange),
         );
      }
      return;
    }
    
    setState(() => _isLoading = true);
    try {
        final success = await _apiClient.requestOtp(_phoneController.text);
        if (success) {
            setState(() => _otpSent = true);
            if (mounted) {
              ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(content: Text('Code sent! (Use 1234)', style: TextStyle(color: Colors.white)), backgroundColor: AppTheme.successGreen),
              );
            }
        } else {
             if (mounted) {
               ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(content: Text('Failed to send code.'), backgroundColor: AppTheme.errorRed),
              );
             }
        }
    } catch (e) {
        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
              const SnackBar(content: Text('Error sending code.'), backgroundColor: AppTheme.errorRed),
          );
        }
    } finally {
        if (mounted) setState(() => _isLoading = false);
    }
  }

  Future<void> _handleVerifyOtp() async {
      if (_otpController.text.length < 4) return;

      setState(() => _isLoading = true);
      try {
          final data = await _apiClient.verifyOtp(_phoneController.text, _otpController.text);
          // Store Producer ID for session
          if (data['producer_id'] != null) {
              ApiClient.currentProducerId = data['producer_id'];
          }
          
          if (mounted) {
              Navigator.pushReplacementNamed(context, '/home');
          }
      } catch (e) {
          if (mounted) {
              ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(content: Text('Invalid Code'), backgroundColor: AppTheme.errorRed),
              );
          }
      } finally {
          if (mounted) setState(() => _isLoading = false);
      }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black, // Fallback
      body: Stack(
        fit: StackFit.expand,
        children: [
          // Background Image
          Image.network(
            "https://images.unsplash.com/photo-1600093463592-8e36ae95ef56?q=80&w=1000&auto=format&fit=crop",
            fit: BoxFit.cover,
            errorBuilder: (ctx, _, __) => Container(color: AppTheme.primaryGreen),
          ),
          
          // Dark Overlay
          Container(
            decoration: BoxDecoration(
              gradient: LinearGradient(
                begin: Alignment.topCenter,
                end: Alignment.bottomCenter,
                colors: [
                  Colors.black.withOpacity(0.3),
                  Colors.black.withOpacity(0.7),
                ],
              ),
            ),
          ),

          // Content
          Center(
            child: SingleChildScrollView(
              padding: const EdgeInsets.all(24.0),
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  // Logo / Title
                  const Icon(Icons.spa_outlined, size: 64, color: AppTheme.accentGold),
                  const SizedBox(height: 16),
                  Text(
                    'TERAVOO',
                    style: AppTheme.textTheme.displayLarge?.copyWith(
                      color: Colors.white,
                      letterSpacing: 4.0,
                    ),
                  ),
                  Text(
                    'PRODUCER CONNECT',
                    style: AppTheme.textTheme.labelLarge?.copyWith(
                      color: Colors.white70,
                      fontWeight: FontWeight.w300,
                    ),
                  ),
                  
                  const SizedBox(height: 48),

                  // Glassmorphism Card
                  ClipRRect(
                    borderRadius: BorderRadius.circular(24),
                    child: BackdropFilter(
                      filter: ImageFilter.blur(sigmaX: 10, sigmaY: 10),
                      child: Container(
                        padding: const EdgeInsets.all(32),
                        decoration: BoxDecoration(
                          color: Colors.white.withOpacity(0.1),
                          borderRadius: BorderRadius.circular(24),
                          border: Border.all(color: Colors.white.withOpacity(0.2)),
                        ),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.stretch,
                          children: [
                             if (!_otpSent) ...[
                                Text("Welcome Back", style: AppTheme.textTheme.headlineMedium?.copyWith(color: Colors.white), textAlign: TextAlign.center),
                                const SizedBox(height: 8),
                                Text("Enter your phone number to access your dashboard.", style: AppTheme.textTheme.bodyMedium?.copyWith(color: Colors.white70), textAlign: TextAlign.center),
                                const SizedBox(height: 32),
                                TextField(
                                  controller: _phoneController,
                                  keyboardType: TextInputType.phone,
                                  cursorColor: AppTheme.accentGold,
                                  style: const TextStyle(color: Colors.white),
                                  decoration: const InputDecoration(
                                    labelText: 'Phone Number',
                                    labelStyle: TextStyle(color: Colors.white70),
                                    prefixText: '+261 ',
                                    prefixStyle: TextStyle(color: Colors.white),
                                    fillColor: Colors.black26, 
                                    prefixIcon: Icon(Icons.phone, color: AppTheme.accentGold),
                                  ),
                                ),
                                const SizedBox(height: 24),
                                ElevatedButton(
                                  onPressed: _isLoading ? null : _handleSendOtp,
                                  style: ElevatedButton.styleFrom(
                                    backgroundColor: AppTheme.accentGold,
                                    foregroundColor: Colors.black,
                                  ),
                                  child: _isLoading 
                                      ? const SizedBox(height: 20, width: 20, child: CircularProgressIndicator(color: Colors.black, strokeWidth: 2))
                                      : const Text('SEND CODE'),
                                ),
                             ] else ...[
                                 Text("Enter Code", style: AppTheme.textTheme.headlineMedium?.copyWith(color: Colors.white), textAlign: TextAlign.center),
                                 const SizedBox(height: 8),
                                 Text("Sent to +261 ${_phoneController.text}", style: AppTheme.textTheme.bodyMedium?.copyWith(color: Colors.white70), textAlign: TextAlign.center),
                                 const SizedBox(height: 32),
                                 TextField(
                                  controller: _otpController,
                                  keyboardType: TextInputType.number,
                                  cursorColor: AppTheme.accentGold,
                                  maxLength: 4,
                                  textAlign: TextAlign.center,
                                  style: const TextStyle(color: Colors.white, fontSize: 24, letterSpacing: 8),
                                  decoration: InputDecoration(
                                    counterText: "",
                                    fillColor: Colors.black26, 
                                    hintText: "••••",
                                    hintStyle: TextStyle(color: Colors.white.withOpacity(0.3)),
                                    border: OutlineInputBorder(borderRadius: BorderRadius.circular(12), borderSide: const BorderSide(color: AppTheme.accentGold)),
                                    focusedBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(12), borderSide: const BorderSide(color: AppTheme.accentGold, width: 2)),
                                  ),
                                ),
                                const SizedBox(height: 24),
                                ElevatedButton(
                                  onPressed: _isLoading ? null : _handleVerifyOtp,
                                  style: ElevatedButton.styleFrom(
                                    backgroundColor: AppTheme.accentGold,
                                    foregroundColor: Colors.black,
                                  ),
                                  child: _isLoading 
                                      ? const SizedBox(height: 20, width: 20, child: CircularProgressIndicator(color: Colors.black, strokeWidth: 2))
                                      : const Text('VERIFY & LOGIN'),
                                ),
                                TextButton(
                                    onPressed: () => setState(() => _otpSent = false),
                                    child: const Text("Use different number", style: TextStyle(color: Colors.white54))
                                )
                             ]
                          ],
                        ),
                      ),
                    ),
                  ),
                  
                  const SizedBox(height: 32),
                  if (!_otpSent)
                    const Text(
                      'By logging in, you accept the Terms of Service for Producers.',
                      textAlign: TextAlign.center,
                      style: TextStyle(fontSize: 12, color: Colors.white30),
                    ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}

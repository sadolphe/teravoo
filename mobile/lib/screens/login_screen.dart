import 'package:flutter/material.dart';
import '../core/api_client.dart';

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
    setState(() => _isLoading = true);
    try {
        final success = await _apiClient.requestOtp(_phoneController.text);
        if (success) {
            setState(() => _otpSent = true);
            ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(content: Text('Code sent! (Use 1234)')),
            );
        } else {
             ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(content: Text('Failed to send code.')),
            );
        }
    } catch (e) {
        ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(content: Text('Error sending code.')),
        );
    } finally {
        if (mounted) setState(() => _isLoading = false);
    }
  }

  Future<void> _handleVerifyOtp() async {
      setState(() => _isLoading = true);
      try {
          final data = await _apiClient.verifyOtp(_phoneController.text, _otpController.text);
          // TODO: Store token securely
          print("Login Success: ${data['role']}");
          
          if (mounted) {
              Navigator.pushReplacementNamed(context, '/home');
          }
      } catch (e) {
          if (mounted) {
              ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(content: Text('Invalid Code')),
              );
          }
      } finally {
          if (mounted) setState(() => _isLoading = false);
      }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Theme.of(context).colorScheme.background,
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(24.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              const Icon(Icons.spa, size: 80, color: Color(0xFF1B5E20)),
              const SizedBox(height: 16),
              const Text(
                'TeraVoo',
                textAlign: TextAlign.center,
                style: TextStyle(fontSize: 32, fontWeight: FontWeight.bold, color: Color(0xFF1B5E20)),
              ),
              const Text(
                'Producer App',
                textAlign: TextAlign.center,
                style: TextStyle(color: Colors.grey),
              ),
              const SizedBox(height: 48),
              
              if (!_otpSent) ...[
                  TextField(
                    controller: _phoneController,
                    keyboardType: TextInputType.phone,
                    decoration: InputDecoration(
                      labelText: 'Phone Number',
                      prefixText: '+261 ',
                      border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
                      filled: true,
                      fillColor: Colors.white,
                    ),
                  ),
                  const SizedBox(height: 24),
                  FilledButton(
                    onPressed: _isLoading ? null : _handleSendOtp,
                    style: FilledButton.styleFrom(
                        padding: const EdgeInsets.symmetric(vertical: 16),
                        backgroundColor: const Color(0xFF1B5E20),
                    ),
                    child: _isLoading 
                        ? const SizedBox(height: 20, width: 20, child: CircularProgressIndicator(color: Colors.white, strokeWidth: 2))
                        : const Text('Send Code', style: TextStyle(fontSize: 16)),
                  ),
              ] else ...[
                   Text("Enter code sent to +261 ${_phoneController.text}", textAlign: TextAlign.center),
                   const SizedBox(height: 16),
                   TextField(
                    controller: _otpController,
                    keyboardType: TextInputType.number,
                    maxLength: 4,
                    textAlign: TextAlign.center,
                    decoration: InputDecoration(
                      hintText: '0000',
                      border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
                      filled: true,
                      fillColor: Colors.white,
                    ),
                  ),
                  const SizedBox(height: 24),
                  FilledButton(
                    onPressed: _isLoading ? null : _handleVerifyOtp,
                    style: FilledButton.styleFrom(
                        padding: const EdgeInsets.symmetric(vertical: 16),
                        backgroundColor: const Color(0xFF1B5E20),
                    ),
                    child: _isLoading 
                        ? const SizedBox(height: 20, width: 20, child: CircularProgressIndicator(color: Colors.white, strokeWidth: 2))
                        : const Text('Verify & Login', style: TextStyle(fontSize: 16)),
                  ),
                  TextButton(
                      onPressed: () => setState(() => _otpSent = false),
                      child: const Text("Use different number")
                  )
              ],
              
              const SizedBox(height: 16),
               if (!_otpSent)
                  const Text(
                    'By logging in, you accept the Terms of Service for Producers.',
                    textAlign: TextAlign.center,
                    style: TextStyle(fontSize: 12, color: Colors.grey),
                  ),
            ],
          ),
        ),
      ),
    );
  }
}

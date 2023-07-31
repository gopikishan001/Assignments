import 'package:flutter/material.dart';
import 'package:weight_tracker/widgets/signinButton.dart';

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        decoration: BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
            colors: [
              const Color.fromARGB(255, 226, 115, 246),
              Color.fromARGB(255, 149, 36, 169),
              Color.fromARGB(255, 71, 26, 148)
            ],
          ),
        ),
        child: Center(
          child: Container(
            height: 300,
            child: Column(
              children: [
                const Text("Track your weight",
                    style: TextStyle(
                      color: Colors.white,
                      fontSize: 30,
                    )),
                SizedBox(height: 50),
                GoogleSignInButton(),
              ],
            ),
          ),
        ),
      ),
    );
  }
}

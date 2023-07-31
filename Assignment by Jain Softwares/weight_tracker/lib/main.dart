// ignore_for_file: must_be_immutable

import 'package:firebase_auth/firebase_auth.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:flutter/services.dart';
import 'package:weight_tracker/screens/login.dart';
import 'package:flutter/material.dart';

import 'screens/home.dart';

Future<void> main() async {
  SystemChrome.setPreferredOrientations([DeviceOrientation.portraitUp]);
  WidgetsFlutterBinding.ensureInitialized();
  await Firebase.initializeApp();

  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  MyApp({Key? key}) : super(key: key);

  User? user = FirebaseAuth.instance.currentUser;

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Flutter Assignment',
      theme: ThemeData(
        primarySwatch: Colors.purple,
      ),
      routes: <String, WidgetBuilder>{
        '/homeScreen': (BuildContext context) => const HomeScreen(),
        '/loginScreen': (BuildContext context) => const LoginScreen(),
      },
      initialRoute: "loginScreen",
      home: user != null ? HomeScreen() : const LoginScreen(),
    );
  }
}

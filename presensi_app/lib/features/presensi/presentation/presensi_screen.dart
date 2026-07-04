import 'dart:convert';
import 'dart:io';
import 'package:flutter/material.dart';
import 'package:camera/camera.dart';
import 'package:geolocator/geolocator.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../auth/providers/auth_provider.dart';
import '../../../core/network/api_service.dart';
import '../../../core/constants/app_constants.dart';

class PresensiScreen extends ConsumerStatefulWidget {
  const PresensiScreen({super.key});

  @override
  ConsumerState<PresensiScreen> createState() => _PresensiScreenState();
}

class _PresensiScreenState extends ConsumerState<PresensiScreen> {
  CameraController? _cameraController;
  final TextEditingController _kesimpulanController = TextEditingController();
  
  bool _isInitializing = true;
  bool _isSubmitting = false;
  
  String _locationStatus = 'Mencari Lokasi...';
  String _validLocationName = '';
  bool _isLocationValid = false;
  
  @override
  void initState() {
    super.initState();
    _initializeCameraAndLocation();
  }
  
  Future<void> _initializeCameraAndLocation() async {
    try {
      // 1. Initialize Camera
      final cameras = await availableCameras();
      final frontCamera = cameras.firstWhere(
        (camera) => camera.lensDirection == CameraLensDirection.front,
        orElse: () => cameras.first,
      );
      
      _cameraController = CameraController(frontCamera, ResolutionPreset.medium);
      await _cameraController!.initialize();
      
      // 2. Initialize Location
      bool serviceEnabled = await Geolocator.isLocationServiceEnabled();
      if (!serviceEnabled) {
        setState(() => _locationStatus = 'Layanan GPS tidak aktif');
        return;
      }
      
      LocationPermission permission = await Geolocator.checkPermission();
      if (permission == LocationPermission.denied) {
        permission = await Geolocator.requestPermission();
        if (permission == LocationPermission.denied) {
          setState(() => _locationStatus = 'Izin lokasi ditolak');
          return;
        }
      }
      
      if (permission == LocationPermission.deniedForever) {
        setState(() => _locationStatus = 'Izin lokasi ditolak permanen');
        return;
      }
      
      Position position = await Geolocator.getCurrentPosition();
      _checkLocationValidity(position.latitude, position.longitude);
      
    } catch (e) {
      setState(() => _locationStatus = 'Error: $e');
    } finally {
      if (mounted) setState(() => _isInitializing = false);
    }
  }
  
  void _checkLocationValidity(double lat, double lng) {
    double minDistance = double.infinity;
    String closestName = '';
    
    for (var loc in AppConstants.daftarLokasi) {
      double distance = Geolocator.distanceBetween(
        lat, lng, loc['lat'] as double, loc['lng'] as double,
      );
      if (distance < minDistance) {
        minDistance = distance;
        closestName = loc['nama'] as String;
      }
    }
    
    if (minDistance <= AppConstants.maxRadius) {
      _isLocationValid = true;
      _validLocationName = closestName;
      _locationStatus = 'Lokasi Valid: $closestName';
    } else {
      _isLocationValid = false;
      _locationStatus = 'Anda jauh dari lokasi kajian (Jarak: ${minDistance.toStringAsFixed(0)}m)';
    }
    setState(() {});
  }
  
  Future<void> _submitPresensi() async {
    if (!_isLocationValid) return;
    if (_cameraController == null || !_cameraController!.value.isInitialized) return;
    
    setState(() => _isSubmitting = true);
    
    try {
      final user = ref.read(authProvider).value;
      if (user == null) throw Exception("User not logged in");
      
      final XFile image = await _cameraController!.takePicture();
      final bytes = await File(image.path).readAsBytes();
      final base64Image = base64Encode(bytes);
      
      final data = {
        'action': 'savePresensi',
        'data': {
          'nama': user.nama,
          'aum': user.aum,
          'kegiatan': 'Pengajian - ${DateTime.now().toIso8601String().split('T')[0]}',
          'kesimpulan': _kesimpulanController.text,
          'lokasiString': _validLocationName,
          'image': base64Image,
        }
      };
      
      final res = await ApiService.post(data);
      if (res['status'] == 'success') {
        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Presensi Berhasil!')));
          Navigator.pop(context, true); // Return true to trigger refresh
        }
      } else {
        throw Exception(res['message'] ?? 'Gagal presensi');
      }
    } catch (e) {
      if (mounted) ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Error: $e')));
    } finally {
      if (mounted) setState(() => _isSubmitting = false);
    }
  }

  @override
  void dispose() {
    _cameraController?.dispose();
    _kesimpulanController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Form Presensi')),
      body: _isInitializing 
        ? const Center(child: CircularProgressIndicator())
        : SingleChildScrollView(
            padding: const EdgeInsets.all(20),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                if (_cameraController != null && _cameraController!.value.isInitialized)
                  Container(
                    height: 300,
                    decoration: BoxDecoration(
                      borderRadius: BorderRadius.circular(16),
                      color: Colors.black,
                    ),
                    clipBehavior: Clip.antiAlias,
                    child: Transform(
                      alignment: Alignment.center,
                      transform: Matrix4.rotationY(3.14159), // Mirror front camera
                      child: CameraPreview(_cameraController!),
                    ),
                  )
                else
                  Container(
                    height: 300,
                    decoration: BoxDecoration(
                      color: Colors.grey[300],
                      borderRadius: BorderRadius.circular(16),
                    ),
                    child: const Center(child: Text('Kamera tidak tersedia')),
                  ),
                const SizedBox(height: 15),
                Container(
                  padding: const EdgeInsets.all(12),
                  decoration: BoxDecoration(
                    color: _isLocationValid ? Colors.green[50] : Colors.red[50],
                    border: Border.all(color: _isLocationValid ? Colors.green : Colors.red),
                    borderRadius: BorderRadius.circular(12),
                  ),
                  child: Text(
                    _locationStatus,
                    style: TextStyle(
                      color: _isLocationValid ? Colors.green[800] : Colors.red[800],
                      fontWeight: FontWeight.bold,
                    ),
                    textAlign: TextAlign.center,
                  ),
                ),
                const SizedBox(height: 15),
                TextField(
                  controller: _kesimpulanController,
                  maxLines: 3,
                  decoration: InputDecoration(
                    hintText: 'Tulis kesimpulan kajian...',
                    filled: true,
                    fillColor: Colors.grey[100],
                    border: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(12),
                      borderSide: BorderSide.none,
                    ),
                  ),
                ),
                const SizedBox(height: 25),
                ElevatedButton(
                  onPressed: (_isLocationValid && !_isSubmitting) ? _submitPresensi : null,
                  child: _isSubmitting 
                    ? const CircularProgressIndicator(color: Colors.white)
                    : const Text('KIRIM DATA', style: TextStyle(fontWeight: FontWeight.bold)),
                ),
              ],
            ),
          ),
    );
  }
}

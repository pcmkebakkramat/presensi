import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../auth/providers/auth_provider.dart';
import '../../presensi/presentation/presensi_screen.dart';
import '../../../core/network/api_service.dart';
import '../../history/utils/pdf_helper.dart';
import '../../profile/presentation/profile_screen.dart';
import '../../profile/presentation/change_password_screen.dart';

class HomeScreen extends ConsumerStatefulWidget {
  const HomeScreen({super.key});

  @override
  ConsumerState<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends ConsumerState<HomeScreen> {
  bool _isLoading = false;
  List<dynamic> _historyList = [];
  String? _fotoBase64;
  String _lastPresensi = '-';
  String _statCount = '0 / 0';
  String _statPercent = '0%';
  bool _isAlreadyPresent = false;
  
  bool get _isTimeValid {
    final now = DateTime.now();
    if (now.weekday != DateTime.sunday) return false;
    final timeVal = now.hour * 100 + now.minute;
    return timeVal >= 500 && timeVal <= 830;
  }
  
  final _startDateController = TextEditingController();
  final _endDateController = TextEditingController();

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      _loadDashboardData();
    });
  }
  
  @override
  void dispose() {
    _startDateController.dispose();
    _endDateController.dispose();
    super.dispose();
  }

  Future<void> _loadDashboardData() async {
    final user = ref.read(authProvider).value;
    if (user == null) return;
    
    setState(() => _isLoading = true);
    try {
      final res = await ApiService.post({
        'action': 'getReport',
        'nama': user.nama,
        'start': _startDateController.text,
        'end': _endDateController.text,
      });
      
      if (mounted) {
        setState(() {
          _historyList = res['history'] ?? [];
          if (res['fotoTerbaru'] != null && res['fotoTerbaru'].toString().isNotEmpty) {
            _fotoBase64 = res['fotoTerbaru'];
          }
          _lastPresensi = res['lastPresensi'] ?? '-';
          
          final now = DateTime.now();
          final todayStr = '${now.day.toString().padLeft(2, '0')}/${now.month.toString().padLeft(2, '0')}/${now.year}';
          _isAlreadyPresent = res['isSudahAbsenHariIni'] == true || _lastPresensi.contains(todayStr);

          if (res['stats'] != null) {
            _statCount = '${res['stats']['userTotal']} / ${res['stats']['globalTotal']}';
            _statPercent = '${res['stats']['percent']}%';
          }
        });
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Error: $e')));
      }
    } finally {
      if (mounted) setState(() => _isLoading = false);
    }
  }

  Future<void> _selectDate(TextEditingController controller) async {
    final DateTime? picked = await showDatePicker(
      context: context,
      initialDate: DateTime.now(),
      firstDate: DateTime(2020),
      lastDate: DateTime(2030),
    );
    if (picked != null) {
      setState(() {
        controller.text = picked.toIso8601String().split('T')[0];
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    final user = ref.watch(authProvider).value;

    return Scaffold(
      body: CustomScrollView(
        slivers: [
          SliverAppBar(
            expandedHeight: 220.0,
            floating: false,
            pinned: true,
            flexibleSpace: FlexibleSpaceBar(
              background: Container(
                decoration: const BoxDecoration(
                  gradient: LinearGradient(
                    colors: [Color(0xFF0F766E), Color(0xFF0D9488)],
                    begin: Alignment.topLeft,
                    end: Alignment.bottomRight,
                  ),
                ),
                padding: const EdgeInsets.only(top: 50, left: 20, right: 20, bottom: 20),
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.end,
                  children: [
                    Row(
                      children: [
                        ClipRRect(
                          borderRadius: BorderRadius.circular(10),
                          child: Container(
                            color: Colors.white.withOpacity(0.2),
                            padding: const EdgeInsets.all(5),
                            child: Image.asset('assets/images/logo.png', width: 40, height: 40),
                          ),
                        ),
                        const SizedBox(width: 12),
                        const Expanded(
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text(
                                'Presensi Kajian AUM',
                                style: TextStyle(color: Colors.white, fontSize: 16, fontWeight: FontWeight.bold),
                              ),
                              Text(
                                'PCM Kebakkramat, Karanganyar',
                                style: TextStyle(color: Colors.white70, fontSize: 12),
                              ),
                            ],
                          ),
                        ),
                        IconButton(
                          icon: const Icon(Icons.menu, color: Colors.white),
                          onPressed: () {
                            showModalBottomSheet(
                              context: context,
                              shape: const RoundedRectangleBorder(
                                borderRadius: BorderRadius.vertical(top: Radius.circular(25)),
                              ),
                              builder: (context) => _buildMenuSheet(context, ref),
                            );
                          },
                        ),
                      ],
                    ),
                    const SizedBox(height: 15),
                    Container(
                      padding: const EdgeInsets.all(12),
                      decoration: BoxDecoration(
                        color: Colors.white.withOpacity(0.1),
                        borderRadius: BorderRadius.circular(16),
                        border: Border.all(color: Colors.white.withOpacity(0.2)),
                      ),
                      child: Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          Expanded(
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Text(
                                  user?.nama ?? 'Nama User',
                                  style: const TextStyle(color: Colors.white, fontWeight: FontWeight.w600, fontSize: 14),
                                ),
                                const SizedBox(height: 2),
                                Text(
                                  (user?.aum != null && user!.aum.isNotEmpty) ? user.aum : 'Asal AUM',
                                  style: TextStyle(color: Colors.white.withOpacity(0.8), fontSize: 12),
                                  maxLines: 2,
                                  overflow: TextOverflow.ellipsis,
                                ),
                              ],
                            ),
                          ),
                        ],
                      ),
                    ),
                  ],
                ),
              ),
            ),
          ),
          SliverToBoxAdapter(
            child: Padding(
              padding: const EdgeInsets.all(20.0),
              child: Column(
                children: [
                  _buildMainCard(),
                  if (_isAlreadyPresent)
                    Container(
                      padding: const EdgeInsets.all(12),
                      decoration: BoxDecoration(color: Colors.green.withOpacity(0.1), borderRadius: BorderRadius.circular(8)),
                      child: const Row(
                        children: [
                          Icon(Icons.check_circle, color: Colors.green),
                          SizedBox(width: 10),
                          Expanded(child: Text('Anda sudah melakukan presensi hari ini.', style: TextStyle(color: Colors.green))),
                        ],
                      ),
                    )
                  else if (!_isTimeValid)
                    Container(
                      padding: const EdgeInsets.all(12),
                      decoration: BoxDecoration(color: Colors.orange.withOpacity(0.1), borderRadius: BorderRadius.circular(8)),
                      child: const Row(
                        children: [
                          Icon(Icons.access_time, color: Colors.orange),
                          SizedBox(width: 10),
                          Expanded(
                            child: Text(
                              'PRESENSI DITUTUP\nJadwal Kajian Di Sini:\nAhad 05:00 - 08:30 WIB.',
                              style: TextStyle(color: Colors.orange, fontWeight: FontWeight.bold),
                            ),
                          ),
                        ],
                      ),
                    ),
                  const SizedBox(height: 15),
                  ElevatedButton(
                    onPressed: (!_isTimeValid || _isAlreadyPresent) ? null : () async {
                      final result = await Navigator.push(
                        context,
                        MaterialPageRoute(builder: (_) => const PresensiScreen()),
                      );
                      if (result == true) {
                        _loadDashboardData();
                      }
                    },
                    style: ElevatedButton.styleFrom(
                      minimumSize: const Size(double.infinity, 55),
                      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
                      disabledBackgroundColor: Colors.grey[300],
                    ),
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Icon(
                          _isAlreadyPresent ? Icons.check_circle : (!_isTimeValid ? Icons.lock_clock : Icons.fingerprint),
                          size: 24,
                          color: (!_isTimeValid || _isAlreadyPresent) ? Colors.grey[600] : Colors.white,
                        ),
                        const SizedBox(width: 10),
                        Text(
                          _isAlreadyPresent ? 'SUDAH PRESENSI' : (!_isTimeValid ? 'PRESENSI DITUTUP' : 'PRESENSI KAJIAN'),
                          style: TextStyle(
                            fontSize: 16, 
                            fontWeight: FontWeight.bold,
                            color: (!_isTimeValid || _isAlreadyPresent) ? Colors.grey[600] : Colors.white,
                          ),
                        ),
                      ],
                    ),
                  ),
                  const SizedBox(height: 30),
                  _buildHistorySection(),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildMainCard() {
    return Container(
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(24),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.05),
            blurRadius: 15,
            offset: const Offset(0, 5),
          ),
        ],
      ),
      padding: const EdgeInsets.all(15),
      child: Column(
        children: [
          Container(
            width: double.infinity,
            height: 200,
            decoration: BoxDecoration(
              color: const Color(0xFFE2E8F0),
              borderRadius: BorderRadius.circular(16),
            ),
            child: _fotoBase64 != null
                ? ClipRRect(
                    borderRadius: BorderRadius.circular(16),
                    child: Image.memory(
                      base64Decode(_fotoBase64!),
                      fit: BoxFit.cover,
                    ),
                  )
                : const Center(
                    child: Text('Belum Ada Foto', style: TextStyle(color: Colors.blueGrey)),
                  ),
          ),
          const SizedBox(height: 15),
          const Text('Terakhir Hadir:', style: TextStyle(color: Colors.blueGrey, fontSize: 12)),
          Text(_lastPresensi, style: const TextStyle(color: Color(0xFF0F766E), fontWeight: FontWeight.bold)),
          const SizedBox(height: 15),
          Row(
            children: [
              Expanded(
                child: Container(
                  padding: const EdgeInsets.all(10),
                  decoration: BoxDecoration(
                    color: const Color(0xFFF8FAFC),
                    borderRadius: BorderRadius.circular(12),
                    border: Border.all(color: const Color(0xFFE2E8F0)),
                  ),
                  child: Column(
                    children: [
                      const Text('KEHADIRAN', style: TextStyle(color: Colors.blueGrey, fontSize: 10)),
                      Text(_statCount, style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
                    ],
                  ),
                ),
              ),
              const SizedBox(width: 10),
              Expanded(
                child: Container(
                  padding: const EdgeInsets.all(10),
                  decoration: BoxDecoration(
                    color: const Color(0xFFF8FAFC),
                    borderRadius: BorderRadius.circular(12),
                    border: Border.all(color: const Color(0xFFE2E8F0)),
                  ),
                  child: Column(
                    children: [
                      const Text('PERSENTASE', style: TextStyle(color: Colors.blueGrey, fontSize: 10)),
                      Text(_statPercent, style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: Color(0xFF0F766E))),
                    ],
                  ),
                ),
              ),
            ],
          )
        ],
      ),
    );
  }

  Widget _buildHistorySection() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text('Riwayat Kehadiran', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
        const SizedBox(height: 15),
        Container(
          padding: const EdgeInsets.all(10),
          decoration: BoxDecoration(
            color: const Color(0xFFF1F5F9),
            borderRadius: BorderRadius.circular(12),
          ),
          child: Row(
            children: [
              Expanded(child: _buildDateField('Mulai', _startDateController)),
              const SizedBox(width: 10),
              Expanded(child: _buildDateField('Selesai', _endDateController)),
              const SizedBox(width: 10),
              Container(
                decoration: BoxDecoration(
                  borderRadius: BorderRadius.circular(8),
                  color: Colors.black87,
                ),
                child: IconButton(
                  icon: const Icon(Icons.search, color: Colors.white, size: 20),
                  onPressed: _loadDashboardData,
                ),
              ),
              const SizedBox(width: 5),
              Container(
                decoration: BoxDecoration(
                  borderRadius: BorderRadius.circular(8),
                  color: Colors.redAccent,
                ),
                child: IconButton(
                  icon: const Icon(Icons.picture_as_pdf, color: Colors.white, size: 20),
                  onPressed: () {
                    final user = ref.read(authProvider).value;
                    if (user != null && _historyList.isNotEmpty) {
                      PdfHelper.generateAndPrintPdf(
                        user: user,
                        historyData: _historyList,
                        startDate: _startDateController.text.isEmpty ? 'Awal' : _startDateController.text,
                        endDate: _endDateController.text.isEmpty ? 'Sekarang' : _endDateController.text,
                      );
                    } else {
                      ScaffoldMessenger.of(context).showSnackBar(
                        const SnackBar(content: Text('Tidak ada data riwayat untuk dicetak.')),
                      );
                    }
                  },
                ),
              ),
            ],
          ),
        ),
        const SizedBox(height: 20),
        _isLoading
          ? const Center(child: CircularProgressIndicator())
          : _historyList.isEmpty
            ? const Center(child: Text('Belum ada riwayat.', style: TextStyle(color: Colors.blueGrey)))
            : ListView.builder(
                shrinkWrap: true,
                physics: const NeverScrollableScrollPhysics(),
                itemCount: _historyList.length,
                itemBuilder: (context, index) {
                  final item = _historyList[index];
                  String lokasi = item['lokasi'] ?? '';
                  if (lokasi.contains('(')) {
                    lokasi = lokasi.split('(')[0].trim();
                  }
                  
                  return Container(
                    margin: const EdgeInsets.only(bottom: 10),
                    padding: const EdgeInsets.all(15),
                    decoration: BoxDecoration(
                      color: Colors.white,
                      borderRadius: BorderRadius.circular(16),
                      border: Border.all(color: const Color(0xFFF1F5F9)),
                    ),
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Expanded(
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text(item['tanggal'] ?? '', style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 14)),
                              const SizedBox(height: 5),
                              Row(
                                children: [
                                  const Icon(Icons.location_on, size: 14, color: Colors.redAccent),
                                  const SizedBox(width: 5),
                                  Expanded(child: Text(lokasi, style: const TextStyle(fontSize: 12, color: Colors.blueGrey))),
                                ],
                              )
                            ],
                          ),
                        ),
                        Container(
                          padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 5),
                          decoration: BoxDecoration(
                            color: Colors.grey[100],
                            borderRadius: BorderRadius.circular(8),
                            border: Border.all(color: Colors.grey[300]!),
                          ),
                          child: Text(item['jam'] ?? '', style: const TextStyle(fontSize: 12, fontWeight: FontWeight.bold)),
                        )
                      ],
                    ),
                  );
                },
              ),
      ],
    );
  }

  Widget _buildDateField(String hint, TextEditingController controller) {
    return InkWell(
      onTap: () => _selectDate(controller),
      child: Container(
        height: 40,
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(8),
        ),
        padding: const EdgeInsets.symmetric(horizontal: 10),
        alignment: Alignment.centerLeft,
        child: Text(
          controller.text.isEmpty ? hint : controller.text,
          style: TextStyle(color: controller.text.isEmpty ? Colors.blueGrey : Colors.black87, fontSize: 12),
        ),
      ),
    );
  }

  Widget _buildMenuSheet(BuildContext context, WidgetRef ref) {
    return Container(
      padding: const EdgeInsets.all(20),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Center(
            child: Container(
              width: 40,
              height: 5,
              decoration: BoxDecoration(
                color: Colors.grey[300],
                borderRadius: BorderRadius.circular(10),
              ),
            ),
          ),
          const SizedBox(height: 20),
          const Text('Menu Aplikasi', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
          const SizedBox(height: 15),
          ListTile(
            leading: Container(
              padding: const EdgeInsets.all(8),
              decoration: BoxDecoration(color: const Color(0xFFF1F5F9), borderRadius: BorderRadius.circular(8)),
              child: const Icon(Icons.person, color: Color(0xFF0F766E)),
            ),
            title: const Text('Profil & Akun'),
            trailing: const Icon(Icons.chevron_right, size: 20),
            onTap: () {
              Navigator.pop(context);
              Navigator.push(context, MaterialPageRoute(builder: (_) => const ProfileScreen()));
            },
          ),
          ListTile(
            leading: Container(
              padding: const EdgeInsets.all(8),
              decoration: BoxDecoration(color: const Color(0xFFF1F5F9), borderRadius: BorderRadius.circular(8)),
              child: const Icon(Icons.lock, color: Color(0xFF0F766E)),
            ),
            title: const Text('Ganti Password'),
            trailing: const Icon(Icons.chevron_right, size: 20),
            onTap: () {
              Navigator.pop(context);
              Navigator.push(context, MaterialPageRoute(builder: (_) => const ChangePasswordScreen()));
            },
          ),
          ListTile(
            leading: Container(
              padding: const EdgeInsets.all(8),
              decoration: BoxDecoration(color: const Color(0xFFF1F5F9), borderRadius: BorderRadius.circular(8)),
              child: const Icon(Icons.help_outline, color: Color(0xFF0F766E)),
            ),
            title: const Text('Panduan & Instalasi'),
            trailing: const Icon(Icons.chevron_right, size: 20),
            onTap: () {
              Navigator.pop(context);
              _showPanduanModal(context);
            },
          ),
          ListTile(
            leading: Container(
              padding: const EdgeInsets.all(8),
              decoration: BoxDecoration(color: const Color(0xFFFEE2E2), borderRadius: BorderRadius.circular(8)),
              child: const Icon(Icons.logout, color: Colors.red),
            ),
            title: const Text('Keluar (Logout)', style: TextStyle(color: Colors.red)),
            onTap: () {
              Navigator.pop(context);
              ref.read(authProvider.notifier).logout();
            },
          ),
        ],
      ),
    );
  }

  void _showPanduanModal(BuildContext context) {
    showDialog(
      context: context,
      builder: (context) {
        return AlertDialog(
          title: const Text('Panduan & Instalasi', style: TextStyle(fontWeight: FontWeight.bold)),
          content: const SingleChildScrollView(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              mainAxisSize: MainAxisSize.min,
              children: [
                Text('Cara Klaim Nama / Daftar Akun:', style: TextStyle(fontWeight: FontWeight.bold)),
                SizedBox(height: 5),
                Text('1. Klik "Klaim Nama / Daftar Akun" di halaman login.\n'
                     '2. Gunakan kotak pencarian untuk menemukan nama Anda.\n'
                     '3. Pilih Asal AUM yang sesuai.\n'
                     '4. Buat Username dan Password Anda.'),
                SizedBox(height: 15),
                Text('Instalasi:', style: TextStyle(fontWeight: FontWeight.bold)),
                SizedBox(height: 5),
                Text('Karena Anda sekarang menggunakan versi Aplikasi Native (Android/iOS), aplikasi ini telah terpasang di layar depan ponsel Anda dan tidak lagi bergantung pada browser seperti versi web sebelumnya. Nikmati fitur yang lebih cepat dan stabil!'),
              ],
            ),
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.pop(context),
              child: const Text('TUTUP', style: TextStyle(color: Color(0xFF0F766E), fontWeight: FontWeight.bold)),
            )
          ],
        );
      },
    );
  }
}

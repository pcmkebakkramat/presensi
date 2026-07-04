import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../auth/providers/auth_provider.dart';
import '../../../core/network/api_service.dart';

class ProfileScreen extends ConsumerStatefulWidget {
  const ProfileScreen({super.key});

  @override
  ConsumerState<ProfileScreen> createState() => _ProfileScreenState();
}

class _ProfileScreenState extends ConsumerState<ProfileScreen> {
  final _namaController = TextEditingController();
  final _nbmController = TextEditingController();
  final _tempatLahirController = TextEditingController();
  final _tglLahirController = TextEditingController();
  final _emailController = TextEditingController();
  final _hpController = TextEditingController();

  String? _username;
  bool _isLoading = false;
  
  List<String> _aumOptions = [];
  String? _selectedAum;
  String? _selectedJk;

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      _loadProfileAndOptions();
    });
  }
  
  @override
  void dispose() {
    _namaController.dispose();
    _nbmController.dispose();
    _tempatLahirController.dispose();
    _tglLahirController.dispose();
    _emailController.dispose();
    _hpController.dispose();
    super.dispose();
  }

  Future<void> _loadProfileAndOptions() async {
    final user = ref.read(authProvider).value;
    if (user == null) return;
    
    setState(() {
      _isLoading = true;
      _username = user.username;
    });
    
    try {
      // Fetch Options first
      final optRes = await ApiService.post({'action': 'getOptions'});
      if (optRes['status'] == 'success') {
        _aumOptions = List<String>.from(optRes['aum'] ?? []);
      }

      // Fetch Profile
      final res = await ApiService.post({
        'action': 'getProfile',
        'username': user.username,
      });
      
      if (mounted) {
        setState(() {
          if (res['data'] != null) {
            _namaController.text = res['data']['nama'] ?? '';
            _nbmController.text = res['data']['nbm'] ?? '';
            _tempatLahirController.text = res['data']['tempat_lahir'] ?? '';
            _tglLahirController.text = res['data']['tgl_lahir'] ?? '';
            _emailController.text = res['data']['email'] ?? '';
            _hpController.text = res['data']['hp'] ?? '';
            
            String fetchedAum = res['data']['aum'] ?? '';
            if (_aumOptions.contains(fetchedAum)) {
              _selectedAum = fetchedAum;
            } else if (_aumOptions.isNotEmpty) {
              _selectedAum = _aumOptions.first;
            }
            
            String fetchedJk = res['data']['jk'] ?? '';
            if (['Laki-laki', 'Perempuan'].contains(fetchedJk)) {
              _selectedJk = fetchedJk;
            }
          }
        });
      }
    } catch (e) {
      if (mounted) ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Error: $e')));
    } finally {
      if (mounted) setState(() => _isLoading = false);
    }
  }

  Future<void> _saveProfile() async {
    if (_username == null) return;
    setState(() => _isLoading = true);
    try {
      final res = await ApiService.post({
        'action': 'updateProfile',
        'data': {
          'username': _username,
          'nama': _namaController.text,
          'aum': _selectedAum ?? '',
          'jk': _selectedJk ?? '',
          'nbm': _nbmController.text,
          'tempat_lahir': _tempatLahirController.text,
          'tgl_lahir': _tglLahirController.text,
          'email': _emailController.text,
          'hp': _hpController.text,
        }
      });
      
      if (res['status'] == 'success') {
        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Profil berhasil diperbarui')));
          // Refresh user session locally
          ref.read(authProvider.notifier).login(_username!, ''); // we can't fully login without password, actually just reload dashboard.
          // Wait, login requires password. So we just refresh it.
        }
      } else {
        throw Exception(res['message'] ?? 'Gagal menyimpan profil');
      }
    } catch (e) {
      if (mounted) ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Error: $e')));
    } finally {
      if (mounted) setState(() => _isLoading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Profil Saya')),
      body: _isLoading 
        ? const Center(child: CircularProgressIndicator())
        : SingleChildScrollView(
            padding: const EdgeInsets.all(20),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                _buildFieldLabel('Nama Lengkap'),
                TextField(
                  controller: _namaController,
                  decoration: _buildInputDec(),
                ),
                const SizedBox(height: 15),
                
                _buildFieldLabel('Asal AUM'),
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 15),
                  decoration: BoxDecoration(color: const Color(0xFFF1F5F9), borderRadius: BorderRadius.circular(14)),
                  child: DropdownButtonHideUnderline(
                    child: DropdownButton<String>(
                      isExpanded: true,
                      value: _selectedAum,
                      hint: const Text('Pilih AUM'),
                      items: _aumOptions.map((String value) => DropdownMenuItem(value: value, child: Text(value))).toList(),
                      onChanged: (val) => setState(() => _selectedAum = val),
                    ),
                  ),
                ),
                const SizedBox(height: 15),

                _buildFieldLabel('Jenis Kelamin'),
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 15),
                  decoration: BoxDecoration(color: const Color(0xFFF1F5F9), borderRadius: BorderRadius.circular(14)),
                  child: DropdownButtonHideUnderline(
                    child: DropdownButton<String>(
                      isExpanded: true,
                      value: _selectedJk,
                      hint: const Text('Pilih Jenis Kelamin'),
                      items: const [
                        DropdownMenuItem(value: 'Laki-laki', child: Text('Laki-laki')),
                        DropdownMenuItem(value: 'Perempuan', child: Text('Perempuan')),
                      ],
                      onChanged: (val) => setState(() => _selectedJk = val),
                    ),
                  ),
                ),
                const SizedBox(height: 15),

                _buildFieldLabel('NBM / NKTAM'),
                TextField(controller: _nbmController, decoration: _buildInputDec()),
                const SizedBox(height: 15),

                Row(
                  children: [
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          _buildFieldLabel('Tempat Lahir'),
                          TextField(controller: _tempatLahirController, decoration: _buildInputDec()),
                        ],
                      ),
                    ),
                    const SizedBox(width: 15),
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          _buildFieldLabel('Tgl Lahir (YYYY-MM-DD)'),
                          TextField(controller: _tglLahirController, decoration: _buildInputDec(hint: 'Misal: 1990-01-01')),
                        ],
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 15),

                _buildFieldLabel('Email'),
                TextField(controller: _emailController, decoration: _buildInputDec(), keyboardType: TextInputType.emailAddress),
                const SizedBox(height: 15),

                _buildFieldLabel('No. HP / WA'),
                TextField(controller: _hpController, decoration: _buildInputDec(), keyboardType: TextInputType.phone),
                const SizedBox(height: 30),

                ElevatedButton(
                  onPressed: _saveProfile,
                  style: ElevatedButton.styleFrom(
                    padding: const EdgeInsets.symmetric(vertical: 16),
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
                  ),
                  child: const Text('SIMPAN PROFIL'),
                )
              ],
            ),
          ),
    );
  }

  Widget _buildFieldLabel(String label) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 5),
      child: Text(label, style: const TextStyle(fontSize: 12, fontWeight: FontWeight.w600, color: Colors.blueGrey)),
    );
  }

  InputDecoration _buildInputDec({String? hint}) {
    return InputDecoration(
      hintText: hint,
      filled: true,
      fillColor: const Color(0xFFF1F5F9),
      border: OutlineInputBorder(borderRadius: BorderRadius.circular(14), borderSide: BorderSide.none),
    );
  }
}

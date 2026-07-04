class UserModel {
  final String username;
  final String nama;
  final String aum;
  final String? jk;
  final String? nbm;
  final String? alamat;
  final String? tempatLahir;
  final String? tglLahir;
  final String? email;
  final String? hp;

  UserModel({
    required this.username,
    required this.nama,
    required this.aum,
    this.jk,
    this.nbm,
    this.alamat,
    this.tempatLahir,
    this.tglLahir,
    this.email,
    this.hp,
  });

  factory UserModel.fromJson(Map<String, dynamic> json) {
    return UserModel(
      username: json['username'] ?? '',
      nama: json['nama'] ?? '',
      aum: json['aum'] ?? '',
      jk: json['jk'],
      nbm: json['nbm'],
      alamat: json['alamat'],
      tempatLahir: json['tempat_lahir'],
      tglLahir: json['tgl_lahir'],
      email: json['email'],
      hp: json['hp'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'username': username,
      'nama': nama,
      'aum': aum,
      'jk': jk,
      'nbm': nbm,
      'alamat': alamat,
      'tempat_lahir': tempatLahir,
      'tgl_lahir': tglLahir,
      'email': email,
      'hp': hp,
    };
  }
}

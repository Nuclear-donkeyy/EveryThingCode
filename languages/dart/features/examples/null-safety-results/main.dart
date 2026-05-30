sealed class ProfileResult {
  const ProfileResult();
}

class Found extends ProfileResult {
  const Found(this.profile);

  final UserProfile profile;
}

class Missing extends ProfileResult {
  const Missing(this.id);

  final String id;
}

class Invalid extends ProfileResult {
  const Invalid(this.id, this.reason);

  final String id;
  final String reason;
}

class UserProfile {
  const UserProfile({required this.id, required this.displayName});

  final String id;
  final String displayName;
}

ProfileResult loadProfile(Map<String, String?> source, String id) {
  if (!source.containsKey(id)) {
    return Missing(id);
  }

  final rawName = source[id];
  if (rawName == null || rawName.trim().isEmpty) {
    return Invalid(id, 'display name is null or blank');
  }

  return Found(UserProfile(id: id, displayName: rawName.trim()));
}

String describe(ProfileResult result) {
  return switch (result) {
    Found(:final profile) => 'Hello, ${profile.displayName} (${profile.id})',
    Missing(:final id) => 'No profile exists for "$id".',
    Invalid(:final id, :final reason) => 'Profile "$id" is invalid: $reason.',
  };
}

void main() {
  final rawProfiles = <String, String?>{
    'ada': ' Ada Lovelace ',
    'blank': '   ',
    'cached-null': null,
  };

  for (final id in ['ada', 'blank', 'cached-null', 'grace']) {
    print(describe(loadProfile(rawProfiles, id)));
  }
}

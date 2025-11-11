/**
 * Unified Level Data Schema
 * 
 * This module defines a consistent schema for level data across the application.
 * It addresses:
 * - DRY principle by centralizing the level structure
 * - Inconsistent naming (mixed English/Spanish, author/creator/usuario)
 * - Poor data validation
 */

/**
 * Normalize level data to a consistent format
 * @param {Object} level - Raw level data
 * @returns {Object} Normalized level object
 */
export function normalizeLevel(level) {
  return {
    // Core identifiers
    id: level.id || '',
    uniqueId: level.uniqueId || level.unique_id || level.accepted_unique_id || level.all_levels_unique_id,
    
    // Level information (English as primary language)
    name: level.name || level.nombre || 'Unknown Level',
    creator: level.creator || level.author || level.creador || level.usuario || 'Unknown',
    
    // Difficulty and stats
    difficulty: level.difficulty || level.dificultad || 'Unrated',
    stars: level.stars || level.estrellas || '0',
    downloads: level.downloads || '0',
    likes: level.likes || '0',
    
    // Song information
    song: level.song || level.song_name || '',
    songArtist: level.song_artist || level.songArtist || '',
    songId: level.song_id || level.songId || '',
    
    // Level metadata
    length: level.length || 'N/A',
    description: level.description || '',
    url: level.url || (level.id ? `https://gdbrowser.com/${level.id}` : ''),
    
    // User who submitted/requested
    requestedBy: normalizeUser(level.requested_by || level.Send || level.accepted_by),
    
    // Timestamps
    requestedAt: level.requested_at || level.accepted_at || level.submission_timestamp || new Date().toISOString(),
    
    // Server information
    serverId: level.server_id || level.serverId || '',
    serverName: level.server_name || level.serverName || '',
    
    // Additional metadata
    importance: level.importance || 50,
    platform: level.platform || 'Discord',
  };
}

/**
 * Normalize user data to a consistent format
 * @param {Object|Array|undefined} userData - Raw user data
 * @returns {Object} Normalized user object
 */
function normalizeUser(userData) {
  if (!userData) {
    return null;
  }
  
  // Handle array format (e.g., Send: ["username"])
  if (Array.isArray(userData)) {
    return {
      username: userData[0] || 'Unknown',
      userId: null,
      displayName: userData[0] || 'Unknown',
      platform: 'Discord'
    };
  }
  
  // Handle object format
  return {
    userId: userData.user_id || userData.userId || userData.discord_user_id || null,
    username: userData.username || userData.submitted_by || 'Unknown',
    displayName: userData.display_name || userData.displayName || userData.username || 'Unknown',
    platform: userData.platform || 'Discord'
  };
}

/**
 * Validate level data
 * @param {Object} level - Level data to validate
 * @returns {Object} Validation result with isValid and errors
 */
export function validateLevel(level) {
  const errors = [];
  
  if (!level.id || level.id.trim() === '') {
    errors.push('Level ID is required');
  }
  
  if (!level.name || level.name.trim() === '') {
    errors.push('Level name is required');
  }
  
  if (!level.creator || level.creator.trim() === '') {
    errors.push('Level creator is required');
  }
  
  return {
    isValid: errors.length === 0,
    errors
  };
}

/**
 * Create a level object with default values
 * @param {string} id - Level ID
 * @param {Object} overrides - Properties to override defaults
 * @returns {Object} Level object with defaults
 */
export function createLevel(id, overrides = {}) {
  const defaultLevel = {
    id: id || '',
    uniqueId: null,
    name: 'Unknown Level',
    creator: 'Unknown',
    difficulty: 'Unrated',
    stars: '0',
    downloads: '0',
    likes: '0',
    song: '',
    songArtist: '',
    songId: '',
    length: 'N/A',
    description: '',
    url: id ? `https://gdbrowser.com/${id}` : '',
    requestedBy: null,
    requestedAt: new Date().toISOString(),
    serverId: '',
    serverName: '',
    importance: 50,
    platform: 'Discord'
  };
  
  return { ...defaultLevel, ...overrides };
}

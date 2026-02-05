# MongoDB initialization script for Docker
# This script runs when MongoDB container starts for the first time

// Switch to admin database
db = db.getSiblingDB('admin');

// Create admin user (if not exists)
try {
    db.createUser({
        user: 'admin',
        pwd: 'password',
        roles: [
            {
                role: 'userAdminAnyDatabase',
                db: 'admin'
            },
            {
                role: 'readWriteAnyDatabase',
                db: 'admin'
            }
        ]
    });
    print('✅ Admin user created');
} catch (e) {
    print('ℹ️  Admin user already exists');
}

// Switch to mflix database
db = db.getSiblingDB('mflix');

// Create application user for mflix database
try {
    db.createUser({
        user: 'mflix_user',
        pwd: 'mflix_password',
        roles: [
            {
                role: 'readWrite',
                db: 'mflix'
            }
        ]
    });
    print('✅ Mflix user created');
} catch (e) {
    print('ℹ️  Mflix user already exists');
}

// Create indexes for better performance
try {
    // Movies collection indexes
    db.movies.createIndex({ "title": "text", "plot": "text", "fullplot": "text" });
    db.movies.createIndex({ "year": 1 });
    db.movies.createIndex({ "genres": 1 });
    db.movies.createIndex({ "type": 1 });
    db.movies.createIndex({ "imdb.rating": -1 });
    db.movies.createIndex({ "tomatoes.viewer.rating": -1 });
    
    // Users collection indexes
    db.users.createIndex({ "email": 1 }, { unique: true });
    db.users.createIndex({ "name": 1 });
    
    // Comments collection indexes
    db.comments.createIndex({ "movie_id": 1 });
    db.comments.createIndex({ "email": 1 });
    db.comments.createIndex({ "name": 1 });
    db.comments.createIndex({ "date": -1 });
    
    print('✅ Database indexes created');
} catch (e) {
    print('⚠️  Error creating indexes: ' + e);
}

// Insert sample data if collections are empty
try {
    if (db.movies.countDocuments() === 0) {
        // Import sample_mflix data (would need to import actual data file)
        print('📋 Movies collection is empty - you may need to import sample_mflix data');
    }
    
    if (db.users.countDocuments() === 0) {
        print('📋 Users collection is empty');
    }
    
    if (db.comments.countDocuments() === 0) {
        print('📋 Comments collection is empty');
    }
} catch (e) {
    print('⚠️  Error checking collections: ' + e);
}

print('🎉 MongoDB initialization completed');
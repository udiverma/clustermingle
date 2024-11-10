from typing import List
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from ..db import models
from sqlalchemy.orm import Session
from fastapi import HTTPException

def create_initial_groups(users: List[models.User], n_clusters: int = 7) -> List[List[int]]:
    """Create initial group assignments based on user similarities"""
    if not users:
        raise HTTPException(status_code=400, detail="No users available for grouping")
    
    # Adjust n_clusters to not exceed number of users
    n_clusters = min(n_clusters, len(users))
    
    # Combine text data from users
    text_data = [
        f"{user.industry} {user.topics} {user.fun_fact or ''}"
        for user in users
    ]
    
    # For very small number of users, use simple distribution
    if len(users) <= n_clusters:
        return [[user.id] for user in users] + [[] for _ in range(n_clusters - len(users))]
    
    try:
        # Create TF-IDF features
        vectorizer = TfidfVectorizer(
            stop_words='english',
            ngram_range=(1, 2),
            max_features=1000
        )
        features = vectorizer.fit_transform(text_data)
        
        # Perform clustering
        kmeans = KMeans(
            n_clusters=n_clusters,
            random_state=42,
            n_init=10
        )
        cluster_labels = kmeans.fit_predict(features)
        
        # Create balanced groups
        groups = [[] for _ in range(n_clusters)]
        for i, label in enumerate(cluster_labels):
            groups[label].append(users[i].id)
        
        # Balance groups if needed
        return balance_groups(groups)
        
    except Exception as e:
        print(f"Clustering error: {str(e)}")
        return create_random_groups(users, n_clusters)

def rotate_groups(previous_groups: List[List[int]], n_clusters: int = 7, db: Session = None) -> List[List[int]]:
    """Generate new group assignments while avoiding previous combinations"""
    # Get all unique user IDs
    all_users = set()
    for group in previous_groups:
        all_users.update(group)
    
    if not all_users:
        raise HTTPException(status_code=400, detail="No users in previous groups")
    
    # Validate that all users exist in database
    if db:
        existing_users = set(u.id for u in db.query(models.User).all())
        invalid_users = all_users - existing_users
        if invalid_users:
            raise HTTPException(
                status_code=400,
                detail=f"Users with IDs {invalid_users} do not exist"
            )
    
    users_list = list(all_users)
    np.random.shuffle(users_list)
    
    # Calculate target size for each group
    target_size = len(users_list) // n_clusters
    remainder = len(users_list) % n_clusters
    
    # Create new groups
    new_groups = [[] for _ in range(n_clusters)]
    user_index = 0
    
    for i in range(n_clusters):
        current_target = target_size + (1 if i < remainder else 0)
        for _ in range(current_target):
            if user_index < len(users_list):
                new_groups[i].append(users_list[user_index])
                user_index += 1
    
    return balance_groups(new_groups)

def balance_groups(groups: List[List[int]]) -> List[List[int]]:
    """Ensure groups are as evenly sized as possible"""
    if not groups:
        return []
    
    # Flatten all users
    all_users = [user for group in groups for user in group]
    if not all_users:
        return groups
    
    # Calculate target size
    target_size = len(all_users) // len(groups)
    remainder = len(all_users) % len(groups)
    
    # Create new balanced groups
    balanced_groups = [[] for _ in range(len(groups))]
    user_index = 0
    
    for i in range(len(groups)):
        current_target = target_size + (1 if i < remainder else 0)
        for _ in range(current_target):
            if user_index < len(all_users):
                balanced_groups[i].append(all_users[user_index])
                user_index += 1
    
    return balanced_groups

def create_random_groups(users: List[models.User], n_clusters: int) -> List[List[int]]:
    """Create random groups as a fallback method"""
    user_ids = [user.id for user in users]
    np.random.shuffle(user_ids)
    
    # Adjust n_clusters if needed
    n_clusters = min(n_clusters, len(users))
    
    # Create groups
    groups = [[] for _ in range(n_clusters)]
    for i, user_id in enumerate(user_ids):
        group_index = i % n_clusters
        groups[group_index].append(user_id)
    
    return balance_groups(groups)
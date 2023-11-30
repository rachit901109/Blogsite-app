import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from blogsite.models import Post



def ibcf_recommendation(user_id):
    # read user post data
    df=pd.read_csv(r'blogsite\post_recommendations\user_post_data.csv')
    df.rename(columns={'Unnamed: 0':'post_id'},inplace=True)
    df.set_index('post_id',inplace=True)
    df.fillna(0, inplace=True)

    # convert to nd array to calculate cosine similarity of mean centerd ratings
    df_np = df.to_numpy()
    # mean centering
    row_avg = np.mean(df_np,axis=1)
    mean_centered = df_np - row_avg.reshape(-1,1)
    # cosine similarity
    cosine_sim_mat = cosine_similarity(mean_centered)
    cosine_sim_data = pd.DataFrame(cosine_sim_mat)
    # print(df.index.name)

    # get indexes of users top 5 rated posts
    user_ratings = df[str(user_id)]
    top_rated = user_ratings.sort_values(ascending=False).index.tolist()[:5]
    top_rated_post = [Post.query.get(i) for i in top_rated]

    rec_post = []
    for i in top_rated:
        # get top 5 similar posts
        # print(i)
        top_similar_post = cosine_sim_data.loc[i].sort_values(ascending=False).index.tolist()[1]
        rec_post.append(Post.query.get(top_similar_post))
        # get top 5 similar posts that user has not rated
        # for j in top_similar_post:
        #     if j not in top_rated_post:
        #         rec_post.append(j)
        #         break
    
    user_rec = {'previously_rated':top_rated_post,'recommended':rec_post}
    return user_rec

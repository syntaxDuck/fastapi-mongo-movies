import React from "react";
import styles from "../../styles/components/movies/MovieRating.module.css";

interface RatingProps {
  rating: number;
  reviewCount?: number;
  source: string;
  styleClass: string;
  altText: string;
}

export const Rating: React.FC<RatingProps> = ({
  rating,
  reviewCount,
  source,
  styleClass,
  altText,
}) => {
  return (
    <div className={styles[styleClass]}>
      <img
        src={source}
        alt={altText}
        onError={(e) => {
          // Handle broken images
          e.currentTarget.style.display = "none";
        }}
      />
      <div className={styles.ratingInfo}>
        <strong>{rating.toFixed(1)} / 10</strong>
        <p>{reviewCount ? `Votes: ${reviewCount}` : "No votes"}</p>
      </div>
    </div>
  );
};

export const TomatoesCriticRating: React.FC<{ tomatoes?: any }> = ({
  tomatoes,
}) => {
  if (
    tomatoes &&
    tomatoes?.critic?.rating !== undefined &&
    tomatoes?.critic !== null
  ) {
    return (
      <Rating
        rating={tomatoes.critic.rating}
        reviewCount={tomatoes.critic.numReviews}
        source="/assets/tomato.png"
        styleClass="tomatoesCriticRating"
        altText="Rotten Tomatoes Critic Rating"
      />
    );
  }
  return null;
};

export const TomatoesViewerRating: React.FC<{ tomatoes?: any }> = ({
  tomatoes,
}) => {
  if (
    tomatoes &&
    tomatoes?.viewer?.rating !== undefined &&
    tomatoes?.viewer !== null
  ) {
    return (
      <Rating
        rating={tomatoes.viewer.rating}
        reviewCount={tomatoes.viewer.numReviews}
        source="/assets/popcorn.png"
        styleClass="tomatoesViewerRating"
        altText="Rotten Tomatoes Viewer Rating"
      />
    );
  }
  return null;
};

export const ImdbRating: React.FC<{ movie?: any }> = ({ movie }) => {
  if (movie && movie?.imdb?.rating !== undefined && movie?.imdb !== null) {
    return (
      <Rating
        rating={movie.imdb.rating}
        reviewCount={movie.imdb.votes}
        source="/assets/imdb.png"
        styleClass="imdbRating"
        altText="IMDb Rating"
      />
    );
  }
  return null;
};

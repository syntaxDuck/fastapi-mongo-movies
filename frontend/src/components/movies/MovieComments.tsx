import React, { useState, useCallback, useId } from "react";
import { commentService } from "../../services/api";
import { motion, AnimatePresence } from "framer-motion";
import { Input, Button } from "../ui";
import styles from "../../styles/components/movies/MovieComments.module.css";
import { useMovieComments } from "../../hooks";

interface MovieCommentsProps {
  movieId?: string;
}

const MovieComments: React.FC<MovieCommentsProps> = ({ movieId = "" }) => {
  const { data: comments = [], isLoading, error, refetch } = useMovieComments(movieId);
  const commentInputId = useId();
  const [newComment, setNewComment] = useState({
    name: "",
    email: "",
    text: "",
  });
  const [submitting, setSubmitting] = useState(false);

  const handleSubmitComment = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newComment.name || !newComment.email || !newComment.text) return;

    try {
      setSubmitting(true);
      await commentService.postComment(movieId, newComment);
      setNewComment({ name: "", email: "", text: "" });
      refetch();
    } catch (err) {
      console.error("Error submitting comment:", err);
    } finally {
      setSubmitting(false);
    }
  };

  const handleRefresh = useCallback(() => {
    refetch();
  }, [refetch]);

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.15,
        delayChildren: 0.2,
      },
    },
  };

  const commentVariants = {
    hidden: {
      opacity: 0,
      y: 20,
      scale: 0.95,
    },
    visible: {
      opacity: 1,
      y: 0,
      scale: 1,
      transition: {
        type: "spring" as const,
        stiffness: 300,
        damping: 30,
      },
    },
    exit: {
      opacity: 0,
      y: -20,
      scale: 0.95,
      transition: { duration: 0.2 },
    },
  };

  const formVariants = {
    hidden: { opacity: 0, y: -20 },
    visible: {
      opacity: 1,
      y: 0,
      transition: {
        type: "spring" as const,
        stiffness: 400,
        damping: 25,
      },
    },
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString("en-US", {
      year: "numeric",
      month: "short",
      day: "numeric",
    });
  };

  if (isLoading) {
    return (
      <motion.div
        className={styles.commentsContainer}
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.5 }}
      >
        <motion.div
          className={styles.commentsHeader}
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.1 }}
        >
          <h2 className={styles.commentsTitle}>Comments</h2>
          <p className={styles.commentsSubtitle}>
            Loading reviews and discussions...
          </p>
        </motion.div>

        <motion.div
          className={styles.skeletonContainer}
          variants={containerVariants}
          initial="hidden"
          animate="visible"
        >
          {Array.from({ length: 4 }, (_, i) => (
            <motion.div
              key={`skeleton-${i}`}
              className={styles.commentSkeleton}
              variants={commentVariants}
              role="status"
              aria-label={`Loading comment ${i + 1}`}
            >
              <div className={styles.skeletonHeader}>
                <div className={styles.skeletonAvatar}></div>
                <div className={styles.skeletonMeta}>
                  <div className={styles.skeletonName}></div>
                  <div className={styles.skeletonDate}></div>
                </div>
              </div>
              <div className={styles.skeletonContent}>
                <div className={styles.skeletonLine}></div>
                <div className={styles.skeletonLine}></div>
                <div className={styles.skeletonLineShort}></div>
              </div>
            </motion.div>
          ))}
        </motion.div>
      </motion.div>
    );
  }

  const hasComments = comments.length > 0 && !error;

  return (
    <motion.div
      className={styles.commentsContainer}
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
    >
      {/* Header */}
      <motion.div
        className={styles.commentsHeader}
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.1 }}
      >
        <h2 className={styles.commentsTitle}>
          Comments {error ? "" : `(${comments.length})`}
        </h2>
        <p className={styles.commentsSubtitle}>
          Join the discussion and share your thoughts
        </p>
      </motion.div>

      {/* Comment Form */}
      <motion.form
        className={styles.commentForm}
        variants={formVariants}
        initial="hidden"
        animate="visible"
        transition={{ delay: 0.2 }}
        onSubmit={handleSubmitComment}
      >
        <div className={styles.formGrid}>
          <Input
            label="Name"
            placeholder="Your name"
            value={newComment.name}
            onChange={(val) =>
              setNewComment((prev) => ({ ...prev, name: val }))
            }
            required
          />
          <Input
            type="email"
            label="Email"
            placeholder="Your email"
            value={newComment.email}
            onChange={(val) =>
              setNewComment((prev) => ({ ...prev, email: val }))
            }
            required
          />
        </div>
        <div className={styles.formField}>
          <label htmlFor={commentInputId} className={styles.formLabel}>
            Comment <span className={styles.required}>*</span>
          </label>
          <textarea
            id={commentInputId}
            placeholder="Share your thoughts about this movie..."
            className={styles.formTextarea}
            value={newComment.text}
            onChange={(e) =>
              setNewComment((prev) => ({ ...prev, text: e.target.value }))
            }
            rows={3}
            required
            maxLength={1000}
          />
          <div className={styles.charCounter}>
            {newComment.text.length}/1000
          </div>
        </div>
        <Button
          type="submit"
          loading={submitting}
          disabled={!newComment.name || !newComment.email || !newComment.text}
          className={styles.submitButton}
          fullWidth
        >
          Post Comment
        </Button>
      </motion.form>

      {/* Comments List */}
      <AnimatePresence mode="wait">
        {hasComments ? (
          <motion.div
            className={styles.commentsList}
            variants={containerVariants}
            initial="hidden"
            animate="visible"
            exit="hidden"
          >
            {comments.map((comment, _) => (
              <motion.div
                key={comment._id}
                className={styles.commentCard}
                variants={commentVariants}
                initial="hidden"
                animate="visible"
                exit="exit"
                whileHover={{
                  y: -2,
                  transition: { duration: 0.2 },
                }}
                layout
                style={{ originY: 0 }}
              >
                <div className={styles.commentHeader}>
                  <div className={styles.commentAvatar}>
                    {comment.name.charAt(0).toUpperCase()}
                  </div>
                  <div className={styles.commentMeta}>
                    <h4 className={styles.commentAuthor}>{comment.name}</h4>
                    <p className={styles.commentDate}>
                      {formatDate(comment.date)}
                    </p>
                  </div>
                </div>
                <p className={styles.commentText}>{comment.text}</p>
              </motion.div>
            ))}
          </motion.div>
        ) : (
          <motion.div
            className={styles.emptyState}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.3 }}
          >
            <div className={styles.emptyIcon}>{"💬"}</div>
            <h3 className={styles.emptyTitle}>{"No comments yet"}</h3>
            <p className={styles.emptyMessage}>
              {"Be the first to share your thoughts about this movie!"}
            </p>
            {error && (
              <motion.button
                className={styles.retryButton}
                onClick={handleRefresh}
                whileHover={{ scale: 1.05, transition: { duration: 0.2 } }}
                whileTap={{ scale: 0.95 }}
              >
                Refresh
              </motion.button>
            )}
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  );
};

export default MovieComments;

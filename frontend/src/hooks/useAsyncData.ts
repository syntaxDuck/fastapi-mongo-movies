import { useState, useEffect, useCallback } from 'react';

interface UseAsyncDataOptions {
  immediate?: boolean;
  onSuccess?: (data: any) => void;
  onError?: (error: Error) => void;
}

interface UseAsyncDataResult<T> {
  data: T[];
  loading: boolean;
  error: string | null;
  refetch: () => Promise<void>;
  setData: (data: T[]) => void;
}

/**
 * Custom hook for standardized async data fetching
 * Eliminates repeated state management patterns across components
 */
export const useAsyncData = <T>(
  fetchFunction: () => Promise<T[]>,
  dependencies: any[] = [],
  options: UseAsyncDataOptions = {}
): UseAsyncDataResult<T> => {
  const { immediate = true, onSuccess, onError } = options;
  
  const [data, setData] = useState<T[]>([]);
  const [loading, setLoading] = useState(immediate);
  const [error, setError] = useState<string | null>(null);

  const fetchData = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      
      const result = await fetchFunction();
      setData(result);
      
      if (onSuccess) {
        onSuccess(result);
      }
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'An error occurred';
      setError(errorMessage);
      
      if (onError && err instanceof Error) {
        onError(err);
      }
    } finally {
      setLoading(false);
    }
  }, [fetchFunction, onSuccess, onError]);

  useEffect(() => {
    if (immediate) {
      fetchData();
    }
  }, [fetchData, immediate, ...dependencies]);

  return {
    data,
    loading,
    error,
    refetch: fetchData,
    setData
  };
};

export default useAsyncData;
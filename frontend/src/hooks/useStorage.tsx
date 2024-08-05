const useStorage = <T,>(key: string) => {
  const setItem = (value: T): void => {
    localStorage.setItem(key, JSON.stringify(value));
  };

  const getItem = (): T | null => {
    const value = localStorage.getItem(key);
    return value ? JSON.parse(value) : null;
  };

  const removeItem = (): void => {
    localStorage.removeItem(key);
  };

  return { setItem, getItem, removeItem };
};

export default useStorage;

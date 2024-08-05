const useStorage = (key: string) => {
  const setItem = (value: unknown) => {
    localStorage.setItem(key, JSON.stringify(value));
  };

  const getItem = () => {
    const value = localStorage.getItem(key);
    return value ? JSON.parse(value) : null;
  };

  const removeItem = () => {
    localStorage.removeItem(key);
  };

  return { setItem, getItem, removeItem };
};

export default useStorage;

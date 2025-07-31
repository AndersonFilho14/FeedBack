/* eslint-disable @typescript-eslint/no-explicit-any */
  export const removerZeros = (data: any) => {
    return Object.entries(data)
      .filter(([, value]) => (value as number) > 0)
      .map(([key, value]) => ({ name: key, value }));
  };
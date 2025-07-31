import { Form } from "antd";

export const FormItem = ({
  children,
  name,
  required = true,
  label
}: {
  children: React.ReactNode,
  name: string,
  required?: boolean,
  label: string
}) => (
  <Form.Item name={name} label={label} required={required}>
    {children}
  </Form.Item>
);

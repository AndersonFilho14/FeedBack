import { Button } from "antd";
import { useRouter } from "next/navigation";
import React from "react";

function FooterForm() {
  const route = useRouter();
  return (
    <div className="w-full flex justify-center items-center gap-10 mt-4">
      <Button
        onClick={() => route.back()}
        className="w-44 h-13 border-5 rounded-lg border-[#727D73] flex justify-center items-center shadow-[0px_4px_22.5px_3px_rgba(0,0,0,0.18)] bg-amber-50 text-2xl hover:bg-gray-100 transition-colors"
      >
        Voltar
      </Button>
      <Button
        htmlType="submit"
        className="w-44 h-13 border-5 rounded-lg border-[#A4B465] flex justify-center items-center shadow-[0px_4px_22.5px_3px_rgba(0,0,0,0.18)] bg-amber-50 text-2xl hover:bg-amber-100 transition-colors"
      >
        Salvar
      </Button>
    </div>
  );
}

export default FooterForm;

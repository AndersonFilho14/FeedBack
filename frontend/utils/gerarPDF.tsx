import html2canvas from "html2canvas";
import jsPDF from "jspdf";

export const gerarPDF = async (elemento: HTMLElement | null) => {
  if (!elemento) return;

  const canvas = await html2canvas(elemento, {
    scale: 2, 
    useCORS: true,
  });

  const imgData = canvas.toDataURL("image/png");

  const pdf = new jsPDF("p", "mm", "a4");
  const pdfWidth = pdf.internal.pageSize.getWidth(); 
  const pdfHeight = pdf.internal.pageSize.getHeight(); 

  const imgWidth = pdfWidth;
  const imgHeight = (canvas.height * imgWidth) / canvas.width;

  let heightLeft = imgHeight;
  let position = 0;

  pdf.addImage(imgData, "PNG", 0, position, imgWidth, imgHeight);

  while (heightLeft > pdfHeight) {
    position -= pdfHeight;
    heightLeft -= pdfHeight;
    pdf.addPage();
    pdf.addImage(imgData, "PNG", 0, position, imgWidth, imgHeight);
  }

  pdf.save("relatorio-desempenho.pdf");
};

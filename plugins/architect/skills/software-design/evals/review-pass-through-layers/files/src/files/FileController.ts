import { FileService } from "./FileService";

export class FileController {
  constructor(private service: FileService) {}

  async download(req, res) {
    const file = await this.service.getFile(req.params.bucket, req.params.key, "aws", "us-east-1", 3, 5000);
    res.send(file.Body);
  }

  async remove(req, res) {
    try {
      await this.service.deleteFile(req.params.bucket, req.params.key, "aws", "us-east-1", 3, 5000);
      res.sendStatus(204);
    } catch (e) {
      if (e.name === "NoSuchKey") return res.sendStatus(404);
      throw e;
    }
  }
}

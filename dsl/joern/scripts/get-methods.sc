import io.circe.Json
import io.circe.syntax._

def mapper(m: Method): Map[String, String] = {
       Map("id" -> m.id.toString ,"fullName" ->  m.fullName, "name" ->  m.name).toMap
       }

@main def exec(cpgFile: String, outFile: String) = {
   importCpg(cpgFile)
   cpg.method.l.filter(_.filename != "<empty>").map(mapper).map(m => m.asJson).l.asJson.toString |> outFile
}
import io.shiftleft.semanticcpg.dotgenerator.{AstGenerator, CdgGenerator, CfgGenerator, DotSerializer}
import io.joern.dataflowengineoss.dotgenerator.DdgGenerator
import io.shiftleft.semanticcpg.dotgenerator.DotSerializer.Graph
import scala.collection.mutable.Map
import scala.collection.immutable.HashSet

@main def exec(cpgFile: String, outDir: String, methodsIds: String, baseGraphs: String) = {

   importCpg(cpgFile)
   
   val ast = new AstGenerator().generate _
   val cfg = new CfgGenerator().generate _
   val ddg = new DdgGenerator().generate _
   val cdg = new CdgGenerator().generate _

   val ids: Array[Long] = methodsIds.split('_').map(id => id.toLong)
   val gen_map = Map("ast" -> ast, "cfg" -> cfg, "ddg" -> ddg, "cdg" -> cdg)
   val base_graphs: Array[String] = baseGraphs.split('_')
   val base_graphs_set = HashSet() ++ base_graphs

   for(id <- ids) {
       var method = cpg.method.id(id).l(0)
       var iter = base_graphs_set.iterator
       var composite_graph: Graph = null
       var base_graph_name = iter.next()

       if (base_graph_name == "pdg") {
               composite_graph = gen_map("ddg")(method) ++ gen_map("cdg")(method)
           } else {
               composite_graph = gen_map(base_graph_name)(method)
        }

       while(iter.hasNext) {
           base_graph_name = iter.next()
           if (base_graph_name == "pdg") {
               composite_graph = composite_graph ++ gen_map("ddg")(method) ++ gen_map("cdg")(method)
           } else {
               composite_graph = composite_graph ++ gen_map(base_graph_name)(method)
           }
           
       }

       DotSerializer.dotGraph(method, composite_graph, withEdgeTypes = true) |> outDir+"/"+method.name+"_"+id+"_base.dot"

   }

}
# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'Encuesta.departamento'
        db.delete_column('encuesta_encuesta', 'departamento_id')


    def backwards(self, orm):
        
        # User chose to not deal with backwards NULL issues for 'Encuesta.departamento'
        raise RuntimeError("Cannot reverse this migration. 'Encuesta.departamento' and its values cannot be restored.")


    models = {
        'encuesta.abusador': {
            'Meta': {'object_name': 'Abusador'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'encuesta.abuso': {
            'Meta': {'object_name': 'Abuso'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'encuesta.actitud': {
            'Meta': {'object_name': 'Actitud'},
            'encuesta': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['encuesta.Encuesta']"}),
            'escuela_ensena': ('django.db.models.fields.IntegerField', [], {}),
            'familia_ensena': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'porque_abuso': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['encuesta.PorqueAbuso']", 'symmetrical': 'False'}),
            'que_piensa': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['encuesta.QuePiensa']", 'symmetrical': 'False'}),
            'que_piensa_victimas': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['encuesta.QuePiensaVictima']", 'symmetrical': 'False'})
        },
        'encuesta.comoparticipo': {
            'Meta': {'object_name': 'ComoParticipo'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'encuesta.conocimiento': {
            'Meta': {'object_name': 'Conocimiento'},
            'abuso': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['encuesta.Abuso']", 'symmetrical': 'False'}),
            'conoce_ley': ('django.db.models.fields.IntegerField', [], {}),
            'donde_aprendio': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['encuesta.DondeAprendio']", 'symmetrical': 'False'}),
            'donde_informarse': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['encuesta.DondeInformarse']", 'symmetrical': 'False'}),
            'encuesta': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['encuesta.Encuesta']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lugares': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['encuesta.LugarAbuso']", 'symmetrical': 'False'}),
            'que_hacer': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['encuesta.QueHacer']", 'symmetrical': 'False'}),
            'quien_abusa': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['encuesta.Abusador']", 'symmetrical': 'False'})
        },
        'encuesta.dondeaprendio': {
            'Meta': {'object_name': 'DondeAprendio'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'encuesta.dondeinformarse': {
            'Meta': {'object_name': 'DondeInformarse'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'encuesta.encuesta': {
            'Meta': {'object_name': 'Encuesta'},
            'area_reside': ('django.db.models.fields.IntegerField', [], {}),
            'codigo': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'comunidad': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lugar.Comunidad']"}),
            'edad': ('django.db.models.fields.IntegerField', [], {}),
            'escolaridad': ('django.db.models.fields.IntegerField', [], {}),
            'estado_civil': ('django.db.models.fields.IntegerField', [], {}),
            'fecha': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iglesia': ('django.db.models.fields.IntegerField', [], {}),
            'importancia_religion': ('django.db.models.fields.IntegerField', [], {}),
            'municipio': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lugar.Municipio']"}),
            'no_hijas': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'no_hijos': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'organizacion': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['encuesta.Organizacion']"}),
            'que_iglesia': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'recolector': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['encuesta.Encuestador']"}),
            'sexo': ('django.db.models.fields.IntegerField', [], {})
        },
        'encuesta.encuestador': {
            'Meta': {'object_name': 'Encuestador'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre_completo': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        'encuesta.estadoactual': {
            'Meta': {'object_name': 'EstadoActual'},
            'donde_van': ('django.db.models.fields.IntegerField', [], {}),
            'encuesta': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['encuesta.Encuesta']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lugares': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['encuesta.LugarAtencion']", 'null': 'True', 'blank': 'True'}),
            'personas_atienden': ('django.db.models.fields.IntegerField', [], {}),
            'problema_comunidad': ('django.db.models.fields.IntegerField', [], {}),
            'problema_pais': ('django.db.models.fields.IntegerField', [], {}),
            'tipo_atencion': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['encuesta.TipoAtencion']", 'null': 'True', 'blank': 'True'})
        },
        'encuesta.familia': {
            'Meta': {'object_name': 'Familia'},
            'adultos': ('django.db.models.fields.IntegerField', [], {}),
            'encuesta': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['encuesta.Encuesta']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jefe': ('django.db.models.fields.IntegerField', [], {}),
            'ocho_diesciseis': ('django.db.models.fields.IntegerField', [], {}),
            'uno_siete': ('django.db.models.fields.IntegerField', [], {}),
            'vive_con': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['encuesta.ViveCon']", 'symmetrical': 'False'})
        },
        'encuesta.lugarabuso': {
            'Meta': {'object_name': 'LugarAbuso'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'encuesta.lugaratencion': {
            'Meta': {'object_name': 'LugarAtencion'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'encuesta.mensajetransmiten': {
            'Meta': {'object_name': 'MensajeTransmiten'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        },
        'encuesta.organizacion': {
            'Meta': {'object_name': 'Organizacion'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'nombre_corto': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'})
        },
        'encuesta.percepcion': {
            'Meta': {'object_name': 'Percepcion'},
            'conoce_abusados': ('django.db.models.fields.IntegerField', [], {}),
            'defender': ('django.db.models.fields.IntegerField', [], {}),
            'encuesta': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['encuesta.Encuesta']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mensaje': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['encuesta.MensajeTransmiten']", 'symmetrical': 'False'}),
            'que_familia': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['encuesta.QueFamilia']", 'symmetrical': 'False'}),
            'quien_debe': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['encuesta.QuienDebe']", 'symmetrical': 'False'}),
            'rol_empresas': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['encuesta.RolEmpresa']", 'symmetrical': 'False'}),
            'rol_estado': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['encuesta.RolEstado']", 'symmetrical': 'False'}),
            'rol_iglesia': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['encuesta.RolIglesia']", 'symmetrical': 'False'}),
            'rol_medios': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['encuesta.RolMedio']", 'symmetrical': 'False'}),
            'rol_ongs': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['encuesta.RolOng']", 'symmetrical': 'False'})
        },
        'encuesta.porqueabuso': {
            'Meta': {'object_name': 'PorqueAbuso'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'encuesta.practica': {
            'Meta': {'object_name': 'Practica'},
            'como': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['encuesta.ComoParticipo']", 'null': 'True', 'blank': 'True'}),
            'encuesta': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['encuesta.Encuesta']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'participa_prevenir': ('django.db.models.fields.IntegerField', [], {}),
            'que_hago_prevenir': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['encuesta.QueHacePrevenir']", 'symmetrical': 'False'}),
            'que_haria': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['encuesta.QueHaria']", 'symmetrical': 'False'})
        },
        'encuesta.quefamilia': {
            'Meta': {'object_name': 'QueFamilia'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'encuesta.quehaceprevenir': {
            'Meta': {'object_name': 'QueHacePrevenir'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'encuesta.quehacer': {
            'Meta': {'object_name': 'QueHacer'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'encuesta.queharia': {
            'Meta': {'object_name': 'QueHaria'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'encuesta.quepiensa': {
            'Meta': {'object_name': 'QuePiensa'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'encuesta.quepiensavictima': {
            'Meta': {'object_name': 'QuePiensaVictima'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'encuesta.quiendebe': {
            'Meta': {'object_name': 'QuienDebe'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'encuesta.rolempresa': {
            'Meta': {'object_name': 'RolEmpresa'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'encuesta.rolestado': {
            'Meta': {'object_name': 'RolEstado'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'encuesta.roliglesia': {
            'Meta': {'object_name': 'RolIglesia'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'encuesta.rolmedio': {
            'Meta': {'object_name': 'RolMedio'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'encuesta.rolong': {
            'Meta': {'object_name': 'RolOng'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'encuesta.tipoatencion': {
            'Meta': {'object_name': 'TipoAtencion'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'encuesta.vivecon': {
            'Meta': {'object_name': 'ViveCon'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'lugar.comunidad': {
            'Meta': {'object_name': 'Comunidad'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'municipio': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lugar.Municipio']"}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '40'})
        },
        'lugar.departamento': {
            'Meta': {'object_name': 'Departamento'},
            'extension': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'unique': 'True', 'null': 'True', 'db_index': 'True'})
        },
        'lugar.municipio': {
            'Meta': {'ordering': "['departamento__nombre']", 'object_name': 'Municipio'},
            'departamento': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lugar.Departamento']"}),
            'extension': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'latitud': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '5', 'blank': 'True'}),
            'longitud': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '5', 'blank': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'unique': 'True', 'null': 'True', 'db_index': 'True'})
        }
    }

    complete_apps = ['encuesta']
